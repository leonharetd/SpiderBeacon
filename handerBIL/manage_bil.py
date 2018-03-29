#!/usr/bin/env Python
# coding:utf-8
from base_bil import BaseBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST
from DBaction.mongo_action import MongoAction


class MembersManageBIL(BaseBIL):

    def __init__(self):
        super(MembersManageBIL, self).__init__()

    def show_group(self):
        """
        显示所有组名,并按照个数分段给前端显示
        :return: 所有用户组
        """
        each_of_line = 8
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        user_info = mongo_action.find("user_info", {})
        group_list = list(set(user["group"] for user in user_info))
        show_list = [group_list[i:i+each_of_line] for i in range(0, len(group_list), each_of_line)]
        return show_list

    def show_group_members(self, group):
        each_of_line = 8
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        user_info = mongo_action.find("user_info", {})
        group_members = filter(lambda x: x["group"] == group, user_info)
        members = list(set(member["username"] for member in group_members))
        members_list = [members[i:i+each_of_line] for i in range(0, len(members), each_of_line)]
        return members_list


class ProjectManageBIL(BaseBIL):

    def __init__(self):
        super(ProjectManageBIL, self).__init__()

    def show_project(self):
        """
        显示所有服务器,
        :return: 所有服务器信息
        """
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        project_list = mongo_action.find("project", {})
        return project_list


if __name__ == "__main__":
    t = MembersManageBIL()
    print t.show_group_members("system")
