#!/usr/bin/env Python
# coding:utf-8
import os
from base_bil import BaseBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST
from DBaction.mongo_action import MongoAction


class SpiderDeployBIL(BaseBIL):

    def __init__(self):
        super(SpiderDeployBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.upload_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def save_upload_file(self, body, file_name):
        with open(os.path.join(self.upload_path, "data", file_name), "wb") as fp:
            fp.write(body)

    def upsert_deploy_info(self, info):
        self.mongo_action.find_and_modify("project_info", {"pack_name": info["pack_name"]}, info)

    def get_deploy_info(self):
        return self.mongo_action.find("project_info", {}, limit=10)


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