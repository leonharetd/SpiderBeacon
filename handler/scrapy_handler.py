#!/usr/bin/env Python
# coding:utf-8
import tornado.web
from datetime import datetime
from base_handler import BaseHandler
from handerBIL.scrapy_bil import ScrapyBIL


class ScrapyHandler(BaseHandler):

    def post(self):
        scrapy_bil = ScrapyBIL()
        action = self.get_argument("action")
        if action == "watcher":

            spider_info = {
                "ip": self.request.remote_ip,
                "start_time": self.get_argument("start_time"),
                "project": self.get_argument("project_name"),
                "spider_name": self.get_argument("spider_name"),
                "page_num": self.get_argument("page_num"),
                "item_num": self.get_argument("item_num"),
                "pagerate": self.get_argument("pagerate"),
                "itemrate": self.get_argument("itemrate"),
                "status": self.get_argument("status"),
                "job_id": self.get_argument("job_id")
            }
            if spider_info["status"] == "start":
                self.write({"job_id": scrapy_bil.get_job_id(project=spider_info["project"], spider_name=spider_info["spider_name"])})
            else:
                self.write({"message": "ok"})
                scrapy_bil.update_info("running_job", {"job_id": spider_info["job_id"],
                                       "project_name": spider_info["project_name"],
                                       "spider_name": spider_info["spider_name"]}, spider_info, s_upsert=True)

                if spider_info["status"] == "finished":
                    scrapy_bil.insert_info("finished_job", spider_info)

