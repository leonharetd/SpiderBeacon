#!/usr/bin/env Python
# coding:utf-8
import tornado.web
from datetime import datetime
from base_handler import BaseHandler
from handerBIL.scrapy_bil import ScrapyBIL


class ScrapyHandler(BaseHandler):

    def post(self):
        scrapy_bil = ScrapyBIL()
        self.write({"message": "ok"})
        action = self.get_argument("action")
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
            }
            if spider_info["status"] == "start":
                # 初始化状态
                pass
            elif spider_info["status"] == "running":
                # 更新状态
                pass
            elif spider_info["finished"] == "finished":
                # 更新
                pass

        print "aaaaa"
