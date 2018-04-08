#!/usr/bin/env Python
# coding:utf-8
import tornado.web
import json
from tornado import gen
from tornado.websocket import WebSocketHandler
from datetime import datetime
from base_handler import BaseHandler
from handerBIL.spider_bil import SpiderUploadBIL, SpiderDeployBIL, SpiderDashBoardBIL


class SpiderDashBoardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        spider_dashboard = SpiderDashBoardBIL()
        group = self.get_secure_cookie("g")
        user_name = self.get_secure_cookie("u")
        pending_jobs = spider_dashboard.get_pending_jobs(group=group, user_name=user_name)
        running_jobs = spider_dashboard.get_running_jobs(group=group, user_name=user_name)
        running_jobs = spider_dashboard.compute_runtime(running_jobs)
        completed_jobs = spider_dashboard.get_completed_jobs(group=group, user_name=user_name)
        self.render('spider_dashboard.html', pending_jobs=pending_jobs, running_jobs=running_jobs, completed_jobs=completed_jobs)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        spider_dashboard = SpiderDashBoardBIL()
        action = self.get_argument("action")
        if action == "run_spiders":
            _id = self.get_argument("project_id")
            schedule = spider_dashboard.find_one_project(_id)
            for ip in schedule["servers"]:
                id_response = yield spider_dashboard.run_spider(ip, schedule["project"], schedule["spider_name"])
                spider_dashboard.insert_running_id(schedule["_id"], ip, schedule["project"], id_response.result())

            spider_dashboard.update_schedule_start_time(_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            spider_dashboard.update_schedule_status(_id, "running")
            self.write({"status": "ok"})
        elif action == "cancel_spiders":
            _id = self.get_argument("project_id")
            servers = spider_dashboard.find_project_deploy_servers(_id)
            for s in servers:
                info = json.loads(s)
                flag = yield spider_dashboard.stop_spider(info["ip"], info["project"], info["running_id"])

            spider_dashboard.update_schedule_status(_id, "canceled")
            spider_dashboard.queue_delete(_id)
            self.write({"status": "ok"})


class SpiderUploadHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        spider_depoly = SpiderUploadBIL()
        deploy_info = spider_depoly.get_deploy_project_info()
        self.render('spider_upload.html', deploy_info=deploy_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        spider_upload = SpiderUploadBIL()
        pack_name = self.request.files["file_data"][0]["filename"]
        project = pack_name.split(".")[0]
        file_metas = self.request.files["file_data"]
        file_path = spider_upload.save_upload_file(file_metas[0]["body"], pack_name)
        deploy_info = {
            "username":  self.get_secure_cookie("u"),
            "group": self.get_secure_cookie("g"),
            "project": project,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "creator": self.get_secure_cookie("u"),
            "version": "_".join([datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), project]),
            "project_path": file_path
        }

        spider_upload.upsert_deploy_project_info(file_path, deploy_info)
        self.write({"message": "ok"})


class SpiderDeployHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        spider_deploy = SpiderDeployBIL()
        group = self.get_secure_cookie("g")
        user_name = self.get_secure_cookie("u")
        groups = spider_deploy.get_project(group=group, user_name=user_name)
        nodes = spider_deploy.get_nodes()
        self.render('spider_deploy.html', groups=groups, spiders=[], nodes=list(nodes))

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


class SpiderFlushHandler(WebSocketHandler):

    def open(self):
        self.spider_deploy = SpiderDeployBIL()

    def on_message(self, message):
        user_name = self.get_secure_cookie("u")
        group = self.get_secure_cookie("g")
        info = json.loads(message)
        if info.get("action", "") == "deploy":
            servers = []
            for ip in info["servers"]:
                try:
                    servers.append("http://{ip}:6800".format(ip=ip.strip()))
                    self.spider_deploy.deploy_spider("http://{ip}:6800".format(ip=ip.strip()), info["project"])
                    self.spider_deploy.create_schedule(info["project"], info["spider"], group,
                                                       user_name, info["period"], servers)
                    self.write_message(json.dumps({"ip": ip, "status": True}))
                except Exception as e:
                    import traceback
                    print traceback.print_exc()

    def check_origin(self, origin):
        return True


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
