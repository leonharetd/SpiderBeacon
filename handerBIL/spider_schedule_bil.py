#!/usr/bin/env Python
# coding:utf-8
import os
from base_bil import BaseBIL
from scrapy_bil import ScrapyBIL, ScrapydBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST, SCRAPYD_API
from DBaction.mongo_action import MongoAction
from DBaction.redis_action import RedisAction


class SipderScheduleBIL(BaseBIL):

    def __init__(self):
        super(SipderScheduleBIL, self).__init__()
        self.redis_action = RedisAction()
        self.scrapyd = ScrapydBIL(SCRAPYD_API)

    def run_job(self, job_id, ip, project, spider_name):
        sid = self.scrapyd.run_spider(ip, project, spider_name)
        self.redis_action.rpush(job_id, sid)
        return sid

    def stop_job(self, job_id, ip, project):
        return self.scrapyd.stop_spider(ip, project, job_id)


if __name__ == "__main__":
    temp = SipderScheduleBIL()
