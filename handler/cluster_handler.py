#!/usr/bin/env Python
# coding:utf-8
from uuid import uuid4
import tornado.web
from handerBIL.base_bil import auth_by_filter
from handerBIL.cluster_bil import ServerManageBIL
from base_handler import BaseHandler


class ClusterDashBoardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        server_manage = ServerManageBIL()
        machines = server_manage.show_servers()
        group = self.get_secure_cookie("g")
        user_name = self.get_secure_cookie("u")
        machines_with_auth = auth_by_filter(machines, group, user_name)
        self.render('cluster_dashboard.html', machines=machines_with_auth)

    @tornado.web.authenticated
    def post(self):
        members_manage = ServerManageBIL()
        groups = members_manage.show_servers()



