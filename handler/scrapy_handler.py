#!/usr/bin/env Python
# coding:utf-8
import tornado.web
from datetime import datetime
from bson.objectid import ObjectId
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
                "project": self.get_argument("project"),
                "spider_name": self.get_argument("spider_name"),
                "page_num": self.get_argument("page_num"),
                "item_num": self.get_argument("item_num"),
                "pagerate": self.get_argument("pagerate"),
                "itemrate": self.get_argument("itemrate"),
                "status": self.get_argument("status"),
                "job_id": ObjectId(self.get_argument("job_id"))
            }
            if spider_info["status"] == "start":
                job_info = scrapy_bil.get_job_info(project=spider_info["project"],
                                                   spider_name=spider_info["spider_name"])
                spider_info["status"] = "running"
                spider_info["job_id"] = job_info["_id"]
                print spider_info
                scrapy_bil.insert_info("job_running", spider_info)

                self.write({"job_id": str(job_info["_id"]), "job_type": job_info["job_type"]})
            elif spider_info["status"] == "running":
                spider_info.pop("status")
                self.write({"message": "ok"})
                scrapy_bil.update_info("job_running", {"job_id": spider_info["job_id"],
                                                       "project": spider_info["project"],
                                                       "spider_name": spider_info["spider_name"]}, {"$set": spider_info})

            elif spider_info["status"] == "finished":
                self.write({"message": "ok"})
                scrapy_bil.update_info("job_running", {"job_id": spider_info["job_id"],
                                                       "project": spider_info["project"],
                                                       "spider_name": spider_info["spider_name"]}, {"$set": spider_info})
                scrapy_bil.insert_info("job_finished", spider_info)
