#!/usr/bin/env Python
# coding:utf-8
from uuid import uuid4
import tornado.web
from handerBIL.base_bil import auth_by_filter
from handerBIL.manage_bil import MembersManageBIL, ProjectManageBIL
from base_handler import BaseHandler


class MembersManageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        members_manage = MembersManageBIL()
        groups = members_manage.show_group()
        group = self.get_secure_cookie("g")
        members = members_manage.show_group_members(group)
        self.render('members_manage.html', groups=groups, members=members)


class ProjectManageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        project_manage = ProjectManageBIL()
        projects = project_manage.show_project()
        group = self.get_secure_cookie("g")
        user_name = self.get_secure_cookie("u")
        auth = auth_by_filter(projects, group, user_name)
        # auth = [
        #     (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #             "create_time": "2018-03-28", 'action': True}),
        #     (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #             "create_time": "2018-03-28", 'action': True}),
        #     (False, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #              "create_time": "2018-03-28", 'action': True}),
        #     (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #             "create_time": "2018-03-28", 'action': True}),
        #     (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #             "create_time": "2018-03-28", 'action': True}),
        #     (False, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #              "create_time": "2018-03-28", 'action': True}),
        #     (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #             "create_time": "2018-03-28", 'action': True}),
        #     (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #             "create_time": "2018-03-28", 'action': True}),
        #     (False, {"name": 1, "group": "root", "user": "*", "creator": "root",
        #              "create_time": "2018-03-28", 'action': True}),
        # ]
        self.render('project_manage.html', projects=auth)

    @tornado.web.authenticated
    def post(self):
        members_manage = ProjectManageBIL()
        groups = members_manage.show_project()