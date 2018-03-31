#!/usr/bin/env Python
# coding:utf-8
from base_bil import BaseBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST
from DBaction.mongo_action import MongoAction


class ClusterManageBIL(BaseBIL):

    def __init__(self):
        super(ClusterManageBIL, self).__init__()

    def show_servers(self):
        """
        显示所有服务器,
        :return: 所有服务器信息
        """
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        project_list = mongo_action.find("machines", {})
        return project_list


if __name__ == "__main__":
    t = ClusterManageBIL()
