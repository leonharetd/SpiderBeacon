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
        self.write({"message": "ok"})
        if action == "watcher":

            spider_info = {
                "ip": self.request.remote_ip,
                "start_time": self.get_argument("start_time"),
                "project_name": self.get_argument("project_name"),
                "spider_name": self.get_argument("spider_name"),
                "page_num": self.get_argument("page_num"),
                "item_num": self.get_argument("item_num"),
                "pagerate": self.get_argument("pagerate"),
                "itemrate": self.get_argument("itemrate"),
                "status": self.get_argument("status"),
                "job_id": self.get_argument("job_id")
            }
            scrapy_bil.update_info({"job_id": spider_info["job_id"],
                                    "project_name": spider_info["project_name"],
                                    "spider_name": spider_info["spider_name"]}, spider_info, s_upsert=True)

            if spider_info["status"] == "finished":
                scrapy_bil.insert_info("job_history", spider_info)

