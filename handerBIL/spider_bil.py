#!/usr/bin/env Python
# coding:utf-8
import os
from tornado import gen
from datetime import datetime
from bson.objectid import ObjectId
from base_bil import BaseBIL, filter_with_username, get_auth
from scrapy_bil import ScrapydBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST, SCRAPYD_API
from DBaction.mongo_action import MongoAction


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

    def create_schedule(self, project, spider, group, user, perid):
        schedule_info = {
            "project": project,
            "spider_name": spider,
            "group": group,
            "user": user,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
        }
        if perid:
            schedule_info["perid"] = perid
            schedule_info["job_type"] = "perid"
            schedule_info["next_time"] = "XXX"
        return self.mongo_action.update_one("schedule", {"project": project, "spider_name": spider}, schedule_info)

class SpiderDashBoardBIL(BaseBIL):

    def __init__(self):
        super(SpiderDashBoardBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)

    @get_auth
    def get_running_jobs(self):
        return self.mongo_action.find("schedule", {"status": "running", "job_type": "normal"})

    @get_auth
    def get_pending_jobs(self):
        return self.mongo_action.find("schedule", {"status": "pending", "job_type": "normal"})

    def get_completed_jobs(self):
        return self.mongo_action.find("schedule", {"job_type": "normal", "status": {"$in": ["finished", "canceled"]}})


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