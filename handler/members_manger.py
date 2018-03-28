#!/usr/bin/env Python
# coding:utf-8
from uuid import uuid4
import tornado.web
from base_handler import BaseHandler


class MembersManageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        cluster = [
            {"name": "m1", "ip": "111.111.111.111", "cpu_avg": 50, "mem_avg": 66, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.112", "cpu_avg": 51, "mem_avg": 68, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.113", "cpu_avg": 52, "mem_avg": 69, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.114", "cpu_avg": 53, "mem_avg": 69, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.115", "cpu_avg": 54, "mem_avg": 69, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.116", "cpu_avg": 55, "mem_avg": 33, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.117", "cpu_avg": 54, "mem_avg": 22, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.118", "cpu_avg": 55, "mem_avg": 6, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.119", "cpu_avg": 53, "mem_avg": 61, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.120", "cpu_avg": 52, "mem_avg": 23, "spider_num": 10, "status": True},
            {"name": "m1", "ip": "111.111.111.121", "cpu_avg": 51, "mem_avg": 54, "spider_num": 10, "status": True},
        ]
        self.render('cluster_dashboard.html', cluster=cluster)
