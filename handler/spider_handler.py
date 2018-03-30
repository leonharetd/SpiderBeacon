#!/usr/bin/env Python
# coding:utf-8
import tornado.web
from datetime import datetime
from base_handler import BaseHandler
from handerBIL.spider_bil import SpiderDeployBIL


class SpiderDashBoardHandler(BaseHandler):

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
        self.render('spider_dashboard.html', cluster=cluster)


class SpiderDeployHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        spider_depoly = SpiderDeployBIL()
        deploy_info = spider_depoly.get_deploy_info()
        self.render('spider_deploy.html', deploy_info=deploy_info)

    @tornado.web.authenticated
    def post(self):
        spider_depoly = SpiderDeployBIL()
        pack_name = self.request.files["file_data"][0]["filename"]
        deploy_info = {
            "username":  self.get_secure_cookie("u"),
            "group": self.get_secure_cookie("g"),
            "pack_name": pack_name,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "creator": self.get_secure_cookie("u"),
            "version": "_".join([datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), pack_name])
        }
        file_metas = self.request.files["file_data"]
        spider_depoly.save_upload_file(file_metas[0]["body"], pack_name)
        spider_depoly.upsert_deploy_info(deploy_info)
        self.write({"message": "ok"})
