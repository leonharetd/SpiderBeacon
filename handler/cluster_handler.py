#!/usr/bin/env Python
# coding:utf-8
from uuid import uuid4
import tornado.web
from handerBIL.cluster_bil import ClusterManageBIL
from base_handler import BaseHandler


class ClusterDashBoardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        server_manage = ClusterManageBIL()
        machines = server_manage.show_servers()
        machines = [
            {"name": "ppt", "ip": "111.111.111.111", "cpu_avg": "0.556", "mem_avg": "0.456",
             "spider_num": 10, "status": True},
            {"name": "ppt", "ip": "111.112.111.111", "cpu_avg": "0.356", "mem_avg": "0.456",
             "spider_num": 2, "status": True},
            {"name": "ppt", "ip": "111.113.111.111", "cpu_avg": "0.456", "mem_avg": "0.456",
             "spider_num": 3, "status": True},
            {"name": "ppt", "ip": "111.114.111.111", "cpu_avg": "0.856", "mem_avg": "0.456",
             "spider_num": 7, "status": True},
            {"name": "ppt", "ip": "111.115.111.111", "cpu_avg": "0.956", "mem_avg": "0.456",
             "spider_num": 8, "status": True},
            {"name": "ppt", "ip": "111.116.111.111", "cpu_avg": "0.656", "mem_avg": "0.456",
             "spider_num": 0, "status": True},
            {"name": "ppt", "ip": "111.117.111.111", "cpu_avg": "0.156", "mem_avg": "0.456",
             "spider_num": 2, "status": True},
            {"name": "ppt", "ip": "111.111.111.111", "cpu_avg": "0.956", "mem_avg": "0.456",
             "spider_num": 1, "status": True},
            {"name": "ppt", "ip": "111.111.111.111", "cpu_avg": "0.256", "mem_avg": "0.456",
             "spider_num": 22, "status": True},
        ]
        self.render('cluster_dashboard.html', machines=machines)

    @tornado.web.authenticated
    def post(self):
        members_manage = ClusterManageBIL()
        groups = members_manage.show_servers()



