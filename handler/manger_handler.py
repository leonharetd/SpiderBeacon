#!/usr/bin/env Python
# coding:utf-8
from datetime import datetime
import hashlib
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

    @tornado.web.authenticated
    def post(self):
        members_manage = MembersManageBIL()
        action = self.get_argument("action")
        group = self.get_argument("group")
        password = self.get_argument("passward")
        authority = self.get_argument("authority")
        if action == "add_group":
            if members_manage.group_name_check(group):
                info = {
                    "username": group,
                    "group": group,
                    "password": hashlib.md5(password).hexdigest(),
                    "authority": int(authority),
                    "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                members_manage.insert_member(info)
                self.write({"result": "ok"})

        elif action == "add_user":
            user_name = self.get_argument("username")
            group = self.get_secure_cookie("g")
            if members_manage.user_name_check(user_name):
                info = {
                    "username": user_name,
                    "group": group,
                    "password": password,
                    "authority": authority,
                    "create_time": datetime.now().strftime("%b %d %Y %H:%M:%S")
                }
                members_manage.insert_member(info)
        elif action == "del_user":
            pass


class ProjectManageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        project_manage = ProjectManageBIL()
        projects = project_manage.show_project()
        group = self.get_secure_cookie("g")
        user_name = self.get_secure_cookie("u")
        auth = auth_by_filter(projects, group, user_name)
        auth = [
            (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
                    "create_time": "2018-03-28", 'action': True}),
            (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
                    "create_time": "2018-03-28", 'action': True}),
            (False, {"name": 1, "group": "root", "user": "*", "creator": "root",
                     "create_time": "2018-03-28", 'action': True}),
            (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
                    "create_time": "2018-03-28", 'action': True}),
            (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
                    "create_time": "2018-03-28", 'action': True}),
            (False, {"name": 1, "group": "root", "user": "*", "creator": "root",
                     "create_time": "2018-03-28", 'action': True}),
            (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
                    "create_time": "2018-03-28", 'action': True}),
            (True, {"name": 1, "group": "root", "user": "*", "creator": "root",
                    "create_time": "2018-03-28", 'action': True}),
            (False, {"name": 1, "group": "root", "user": "*", "creator": "root",
                     "create_time": "2018-03-28", 'action': True})
        ]
        self.render('project_manage.html', projects=auth)

    @tornado.web.authenticated
    def post(self):
        members_manage = ProjectManageBIL()
        groups = members_manage.show_project()