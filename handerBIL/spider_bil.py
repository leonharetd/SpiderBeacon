#!/usr/bin/env Python
# coding:utf-8
import os
import json
from tornado import gen
from datetime import datetime
from bson.objectid import ObjectId
from base_bil import BaseBIL, filter_with_username, get_auth
from scrapy_bil import ScrapydBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST, SCRAPYD_API
from DBaction.mongo_action import MongoAction
from DBaction.redis_action import RedisAction


class SpiderUploadBIL(BaseBIL):

    def __init__(self):
        super(SpiderUploadBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.upload_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.scrapyd = ScrapydBIL(SCRAPYD_API)

    def save_upload_file(self, body, file_name):
        with open(os.path.join(self.upload_path, "data", file_name), "wb") as fp:
            fp.write(body)
        return os.path.join(self.upload_path, "data", file_name)

    def upsert_deploy_project_info(self, file_path, info):
        spiders_name = self.scrapyd.get_deploy_project_spiders_name(SCRAPYD_API, info["project"], info["version"], file_path)
        info["spiders_name"] = spiders_name
        self.mongo_action.find_and_modify("project_info", {"project": info["project"]}, info)

    def get_deploy_project_info(self):
        return self.mongo_action.find("project_info", {}, limit=10).sort("create_time", -1)


class SpiderDeployBIL(BaseBIL):

    def __init__(self):
        super(SpiderDeployBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.scrapyd = ScrapydBIL(SCRAPYD_API)

    @filter_with_username
    def get_project(self, group, user_name):
        return self.mongo_action.find("project_info", {"group": group})

    def get_spiders(self, project_id):
        return self.mongo_action.find_one("project_info", {"_id": ObjectId(project_id)}, {"_id": 0})

    def get_project_info(self, project_id):
        return self.mongo_action.find_one("project_info", {"_id": ObjectId(project_id)}, {"_id": 0})

    def get_nodes(self):
        return self.mongo_action.find("nodes_info", {})

    @gen.coroutine
    def deploy_spider(self, ip, project):
        file_info = self.mongo_action.find_one("project_info", {"project": project})
        return self.scrapyd.deploy_spider(ip, project, file_info["version"], file_info["project_path"])

    def create_schedule(self, project, spider, group, user, period, job_type, servers):
        schedule_info = {
            "project": project,
            "spider_name": spider,
            "group": group,
            "username": user,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "start_time": "",
            "status": "pending",
            "job_type": job_type,
            "period_value": "",
            "period": period,
            "servers": servers
        }
        if period in ["Period"]:
            schedule_info["job_type"] = ""
            schedule_info["next_time"] = "XXX"
        return self.mongo_action.update_one("schedule", {"project": project,
                                                         "spider_name": spider,
                                                         "create_time": schedule_info["create_time"]},
                                            schedule_info, upsert=True)


class SpiderDashBoardBIL(BaseBIL):

    def __init__(self):
        super(SpiderDashBoardBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.redis_action = RedisAction()
        self.scrapyd = ScrapydBIL(SCRAPYD_API)

    @get_auth
    def get_running_jobs(self, **kwargs):
        return self.mongo_action.find("schedule", {"status": "running",
                                                   "job_type": {"$in": kwargs["job_type"]}})

    @get_auth
    def get_pending_jobs(self, **kwargs):
        return self.mongo_action.find("schedule", {"status": "pending",
                                                   "job_type": {"$in": kwargs["job_type"]}})

    def get_completed_jobs(self, **kwargs):
        return self.mongo_action.find("schedule", {"status": {"$in": ["finished", "canceled"]},
                                                   "job_type": {"$in": kwargs["job_type"]}})

    @gen.coroutine
    def run_spider(self, ip, project, spider_name):
        return self.scrapyd.run_spider(ip, project, spider_name)

    @gen.coroutine
    def stop_spider(self, ip, project, _id):
        return self.scrapyd.stop_spider(ip, project, _id)

    def insert_running_id(self, pid, ip, project, running_id):
        info = {
            "ip": ip,
            "project": project,
            "running_id": running_id
        }
        self.redis_action.rpush(pid, json.dumps(info))

    def queue_delete(self, name):
        return self.redis_action.queue_delete(name)

    def update_schedule_status(self, _id, status):
        self.mongo_action.update_one("schedule", {"_id": ObjectId(_id)}, {"$set": {"status": status}})

    def update_schedule_start_time(self, _id, start_time):
        self.mongo_action.update_one("schedule", {"_id": ObjectId(_id)}, {"$set": {"start_time": start_time}})

    def update_finished_schedule(self, _id, run_time, status):
        self.mongo_action.update_one("schedule", {"_id": ObjectId(_id)}, {"$set": {"status": status, "run_time": run_time}})

    def find_one_project(self, _id):
        return self.mongo_action.find_one("schedule", {"_id": ObjectId(_id)})

    def find_project_deploy_servers(self, _id):
        return self.redis_action.get_list(_id)

    def compute_runtime(self, job):
        now = datetime.now()
        delta = str(now - datetime.strptime(job["start_time"], "%Y-%m-%d %H:%M:%S"))
        delta[:delta.find(".")].replace(":", " : ")
        job["run_time"] = delta[:delta.find(".")].replace(":", " h  ", 1).replace(":", " m ", 1)
        return job

    def get_jobs_without_auth(self, collection, query):
        return self.mongo_action.find(collection, query)

    def update_many_jobs_status(self, query, status):
        self.mongo_action.update_many("schedule", query, {"$set": {"status": status}})

    def add_job_chart(self, name, value):
        self.redis_action.set(name, value)

    def delete_schedule(self, _id):
        self.mongo_action.delete_one("schedule", {"_id": ObjectId(_id)})


class SpiderDashboardDetailBIL(BaseBIL):

    def __init__(self):
        super(SpiderDashboardDetailBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)

    def get_project_job(self, project_id):
        return self.mongo_action.find("job_running", {"job_id": ObjectId(project_id)})


class ProjectManageBIL(BaseBIL):

    def __init__(self):
        super(ProjectManageBIL, self).__init__()

    def show_project(self):
        """
        显示所有服务器,
        :return: 所有服务器信息
        """
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        project_list = mongo_action.find("project_info", {})
        return project_list


if __name__ == "__main__":
    pass