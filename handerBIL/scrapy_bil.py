#!/usr/bin/env Python
# coding:utf-8
import os
from tornado import gen
from base_bil import BaseBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST, SCRAPYD_API
from DBaction.mongo_action import MongoAction
from DBaction.redis_action import RedisAction
from scrapyd_api import ScrapydAPI


class ScrapydBIL(BaseBIL):
    def __init__(self, ip):
        super(ScrapydBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.redis_action = RedisAction()
        self.scrapyd = ScrapydAPI(ip)

    @gen.coroutine
    def deploy_spider(self, ip, project, version, egg):
        sd = ScrapydAPI(ip)
        with open(egg) as fp:
            return sd.add_version(project, version, fp)

    def get_deploy_project_spiders_name(self, ip, project, version, egg):
        self.deploy_spider(ip, project, version, egg)
        spiders_name = self.scrapyd.list_spiders(project)
        return spiders_name

    @gen.coroutine
    def run_spider(self, ip, project, spider_name):
        sd = ScrapydAPI(ip)
        return sd.schedule(project, spider_name)

    @gen.coroutine
    def stop_spider(self, ip, project, id):
        sd = ScrapydAPI(ip)
        return sd.cancel(project, id)


class ScrapyBIL(BaseBIL):
    def __init__(self):
        super(ScrapyBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.redis_action = RedisAction()

    def insert_info(self, collection, info):
        self.mongo_action.insert(collection, info)

    def get_job_info(self, project, spider_name):
        return self.mongo_action.find_one("schedule", {"project": project, "spider_name": spider_name})

    def update_info(self, collection, query, info, **kwargs):
        self.mongo_action.update_one(collection, query, info, **kwargs)


if __name__ == "__main__":
    temp = ScrapyBIL()
    from datetime import datetime
    from bson.objectid import ObjectId
    print  ObjectId.from_datetime(generation_time=datetime.now())

