#!/usr/bin/env Python
# coding:utf-8
from datetime import datetime
import hashlib
import tornado.web
from handerBIL.manage_bil import MembersManageBIL, ProjectManageBIL
from base_handler import BaseHandler


class MembersManageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        members_manage = MembersManageBIL()
        all_groups = members_manage.show_group()
        group = self.get_secure_cookie("g")
        user_name = self.get_secure_cookie("u")
        create_groups = members_manage.get_create_group(creator=user_name)

        group_members = members_manage.filter_group_members(group=group)
        members = members_manage.get_format_group_members(group_members)
        self.render('members_manage.html', all_groups=all_groups, creator_group=create_groups,
                    group_members=group_members, members=members, group_name=group.upper())

    @tornado.web.authenticated
    def post(self):
        members_manage = MembersManageBIL()
        action = self.get_argument("action")
        group = self.get_argument("group")
        status = ""
        if action.startswith("add"):
            password = self.get_argument("passward")
            authority = self.get_argument("authority")
            if action == "add_group":
                status = members_manage.add_group(group, password, authority, self.get_secure_cookie("u"))
                self.write({"result": "{0}".format(status)})
            elif action == "add_user":
                user_name = self.get_argument("username")
                group = self.get_secure_cookie("g")
                status = members_manage.add_user(group, user_name, password, authority, self.get_secure_cookie("u"))
        elif action.startswith("del"):
            if action == "del_group":
                status = members_manage.change_delete_group_relation(group, self.get_secure_cookie("g"),
                                                                     self.get_secure_cookie("u"))
            elif action == "del_user":
                user_name = self.get_argument("username")
                group = self.get_secure_cookie("g")
                status = members_manage.change_delete_user_relation(group, user_name, self.get_secure_cookie("u"))
        self.write({"result": "{0}".format(status)})


class ProjectManageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        group = self.get_secure_cookie("g")
        user_name = self.get_secure_cookie("u")
        project_manage = ProjectManageBIL()
        projects = project_manage.get_project_auth(group=group, username=user_name)
        self.render('project_manage.html', projects=projects)

    @tornado.web.authenticated
    def post(self):
        members_manage = ProjectManageBIL()
        groups = members_manage.get_project_auth()
