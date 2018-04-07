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
        # machines = [
        #     {"name": "ppt", "ip": "111.111.111.111", "cpu_avg": 55, "mem_avg": "0.4561",
        #      "spider_num": 10, "status": True},
        #     {"name": "ppt", "ip": "111.112.111.111", "cpu_avg": 35, "mem_avg": "0.4562",
        #      "spider_num": 2, "status": True},
        #     {"name": "ppt", "ip": "111.113.111.111", "cpu_avg": 45, "mem_avg": "0.4563",
        #      "spider_num": 3, "status": True},
        #     {"name": "ppt", "ip": "111.114.111.111", "cpu_avg": 85, "mem_avg": "0.4564",
        #      "spider_num": 7, "status": True},
        #     {"name": "ppt", "ip": "111.115.111.111", "cpu_avg": 95, "mem_avg": "0.4565",
        #      "spider_num": 8, "status": False},
        #     {"name": "ppt", "ip": "111.116.111.111", "cpu_avg": 65, "mem_avg": "0.4566",
        #      "spider_num": 0, "status": True},
        #     {"name": "ppt", "ip": "111.117.111.111", "cpu_avg": 15, "mem_avg": "0.4567",
        #      "spider_num": 2, "status": True},
        #     {"name": "ppt", "ip": "111.111.111.111", "cpu_avg": 95, "mem_avg": "0.4568",
        #      "spider_num": 1, "status": True},
        #     {"name": "ppt", "ip": "111.111.111.111", "cpu_avg": 25, "mem_avg": "0.4569",
        #      "spider_num": 22, "status": True},
        # ]
        self.render('cluster_dashboard.html', machines=machines)

    @tornado.web.authenticated
    def post(self):
        members_manage = ClusterManageBIL()
        groups = members_manage.show_servers()



