#!/usr/bin/env Python
# coding:utf-8
import os
from bson.objectid import ObjectId
from base_bil import BaseBIL, filter_with_username
from scrapy_bil import ScrapyBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST, SCRAPYD_API
from DBaction.mongo_action import MongoAction


class SpiderUploadBIL(BaseBIL):

    def __init__(self):
        super(SpiderUploadBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.upload_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.scrapyd = ScrapyBIL(SCRAPYD_API)

    def save_upload_file(self, body, file_name):
        with open(os.path.join(self.upload_path, "data", file_name), "wb") as fp:
            fp.write(body)
        return os.path.join(self.upload_path, "data", file_name)

    def upsert_deploy_project_info(self, file_path, info):
        spiders_name = self.scrapyd.get_deploy_project_spiders_name(info["project"], info["version"], file_path)
        info["spiders_name"] = spiders_name
        self.mongo_action.find_and_modify("project_info", {"project": info["project"]}, info)

    def get_deploy_project_info(self):
        return self.mongo_action.find("project_info", {}, limit=10).sort("create_time", -1)




class SpiderDeployBIL(BaseBIL):

    def __init__(self):
        super(SpiderDeployBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.scrapyd = ScrapyBIL(SCRAPYD_API)

    @filter_with_username
    def get_project(self, group, user_name):
        return self.mongo_action.find("project_info", {"group": group})

    def get_spiders(self, project_id):
        return self.mongo_action.find_one("project_info", {"_id": ObjectId(project_id)}, {"_id": 0})

    def get_project_info(self, project_id):
        return self.mongo_action.find_one("project_info", {"_id": ObjectId(project_id)}, {"_id": 0})

    def create_schecule(self, ):

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