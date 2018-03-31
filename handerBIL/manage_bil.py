#!/usr/bin/env Python
# coding:utf-8
from base_bil import BaseBIL
from base_bil import get_auth, filter_with_group
from DBaction.settings import MONGODB_PORT, MONGODB_HOST
from DBaction.mongo_action import MongoAction


class MembersManageBIL(BaseBIL):

    def __init__(self):
        super(MembersManageBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)

    def show_group(self):
        """
        显示所有组名,并按照个数分段给前端显示
        :return: 所有用户组
        """
        each_of_line = 8
        user_info = self.mongo_action.find("user_info", {})
        group_list = list(set(user["group"] for user in user_info))
        show_list = [group_list[i:i+each_of_line] for i in range(0, len(group_list), each_of_line)]
        return show_list

    @filter_with_group
    def filter_group_members(self, **kwargs):
        user_info = self.mongo_action.find("user_info", {})
        return user_info

    def get_group_members(self, group_members):
        each_of_line = 8
        members = list(set(member["username"] for member in group_members))
        members_list = [members[i:i+each_of_line] for i in range(0, len(members), each_of_line)]
        return members_list

    def group_name_check(self, group_name):
        user_info = self.mongo_action.find_one("user_info", {"group": group_name})
        if user_info:
            return False
        return True

    def user_name_check(self, user_name):
        user_info = self.mongo_action.find("user_info", {"user_name": user_name})
        if user_info:
            return False
        return True

    def insert_member(self, info):
        self.mongo_action.insert("user_info", info)

    def delete_member(self, info):
        member = self.mongo_action.find_one("user_info", {"group": info["group"], "username": info["username"]})
        self.mongo_action.delete_one("user_info", {"_id": member["_id"]})


class ProjectManageBIL(BaseBIL):

    def __init__(self):
        super(ProjectManageBIL, self).__init__()

    @get_auth
    def get_project_auth(self, **kwargs):
        """
        显示所有服务器,
        :return: 所有服务器信息
        """
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        project_list = mongo_action.find("project_info", {})
        return project_list


if __name__ == "__main__":
    t = ProjectManageBIL()
    print t.get_project_auth(group="root", username="system")
