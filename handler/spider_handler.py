#!/usr/bin/env Python
# coding:utf-8
import tornado.web
import tornado.gen
from datetime import datetime
from base_handler import BaseHandler
from handerBIL.spider_bil import SpiderUploadBIL, SpiderDeployBIL


class SpiderDashBoardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        cluster = [
            {"name": "m1wwwww", "ip": "111.111.111.111", "cpu_avg": 50, "mem_avg": 66, "spider_num": 10, "status": True},
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


class SpiderUploadHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        spider_depoly = SpiderUploadBIL()
        deploy_info = spider_depoly.get_deploy_project_info()
        self.render('spider_upload.html', deploy_info=deploy_info)

    @tornado.web.authenticated
    def post(self):
        spider_upload = SpiderUploadBIL()
        pack_name = self.request.files["file_data"][0]["filename"]
        project = pack_name.split(".")[0]
        deploy_info = {
            "username":  self.get_secure_cookie("u"),
            "group": self.get_secure_cookie("g"),
            "project": project,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "creator": self.get_secure_cookie("u"),
            "version": "_".join([datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), project])
        }
        file_metas = self.request.files["file_data"]
        file_path = spider_upload.save_upload_file(file_metas[0]["body"], project)
        print file_path
        spider_upload.upsert_deploy_project_info(file_path, deploy_info)
        self.write({"message": "ok"})


class SpiderDeployHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        spider_deploy = SpiderDeployBIL()
        group = self.get_secure_cookie("g")
        user_name = self.get_secure_cookie("u")
        groups = spider_deploy.get_project(group=group, user_name=user_name)
        self.render('spider_deploy.html', groups=groups, spiders=[])

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def post(self):
        spider_deploy = SpiderDeployBIL()
        action = self.get_argument("action")
        if action == "get_spiders":
            project_id = self.get_argument("project_id")
            spiders = spider_deploy.get_spiders(project_id)["spiders_name"]
            self.write({"status": "ok", "message": spiders})
        elif action == "get_project_info":
            project_id = self.get_argument("project_id")
            spider_info = spider_deploy.get_project_info(project_id)
            self.write({"status": "ok", "message": spider_info})
        elif action == "deploy":
            project = self.get_argument("project")
            spider = self.get_argument("spider")
            spider = self.get_argument("peird")
            servers = self.get_argument("servers")
            client = spider_deploy.
            for ip in servers:
                response = yield tornado.gen.Task(client, "{ip}:6800".format(ip=ip))
            self.write("Hello World")
            self.finish()






class SpiderDashBoardDetailHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        cluster = [
            {"name": "mqqqq", "ip": "111.111.111.111", "cpu_avg": 50, "mem_avg": 66, "spider_num": 10, "status": True},
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
        self.render('spider_dashboard_detail.html', machines=cluster)
