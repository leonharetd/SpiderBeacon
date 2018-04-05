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
        members = members_manage.filter_group_members(group=group)
        members = members_manage.get_format_group_members(members)
        user_by_group = members_manage.get_members_user(user_name)
        self.render('members_manage.html', all_groups=all_groups, creator_group=create_groups,
                    user_by_group={g[0]: map(lambda x: x["username"], g[1]) for g in user_by_group}, members=members)

    @tornado.web.authenticated
    def post(self):
        members_manage = MembersManageBIL()
        action = self.get_argument("action")
        group = self.get_argument("group")
        if action.startswith("add"):
            password = self.get_argument("passward")
            authority = self.get_argument("authority")
            if action == "add_group":
                if not members_manage.group_name_exists(group):
                    info = {
                        "username": group,
                        "group": group,
                        "password": hashlib.md5(password).hexdigest(),
                        "authority": int(authority),
                        "creator": self.get_secure_cookie("u"),
                        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    members_manage.insert_member(info)
                    self.write({"result": "ok"})
            elif action == "add_user":
                user_name = self.get_argument("username")
                group = self.get_secure_cookie("g")
                if not members_manage.user_name_exists(user_name):
                    info = {
                        "username": user_name,
                        "group": group,
                        "password": password,
                        "authority": authority,
                        "creator": self.get_secure_cookie("u"),
                        "create_time": datetime.now().strftime("%b %d %Y %H:%M:%S")
                    }
                    members_manage.insert_member(info)
                    self.write({"result": "user add"})
        elif action.startswith("del"):
            if action == "del_group":
                new_group = self.get_secure_cookie("g")
                members_manage.delete_member({"group": group, 'username': group})
                members_manage.update_members({"group": group}, {"$set": {"group": new_group}})
                members_manage.update_members({"creator": group}, {"$set": {"creator": self.get_secure_cookie("u")}})
                members_manage.change_projects_member("project_info", {"group": group}, {"$set": {"group": new_group}})
                members_manage.change_projects_member("job_running", {"group": group}, {"$set": {"group": new_group}})
                self.write({"result": "group delete"})
                # todo 定时任务的修改
            elif action == "del_user":
                new_user = self.get_secure_cookie("u")
                user_name = self.get_argument("username")
                members_manage.update_members({"creator": user_name}, {"$set": {"creator": new_user}})
                members_manage.change_projects_member("project_info", {"creator": user_name}, {"$set": {"creator": new_user}})
                members_manage.change_projects_member("job_running", {"creator": user_name}, {"$set": {"creator": new_user}})
                # todo 定时任务的修改


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
