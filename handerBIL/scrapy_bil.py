#!/usr/bin/env Python
# coding:utf-8
import os
from base_bil import BaseBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST, SCRAPYD_API
from DBaction.mongo_action import MongoAction
from DBaction.redis_action import RedisAction
from scrapyd_api import ScrapydAPI


class ScrapyBIL(BaseBIL):

    def __init__(self, ip):
        super(ScrapyBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.redis_action = RedisAction()
        self.scrapyd = ScrapydAPI(ip)

    def deploy_spider(self, project, version, egg):
        with open(egg) as fp:
            print fp
            return self.scrapyd.add_version(project, version, fp)

    def get_deploy_project_spiders_name(self, project, version, egg):
        print '#', egg
        self.deploy_spider(project, version, egg)
        spiders_name = self.scrapyd.list_spiders(project)
        return spiders_name

    def run_spider(self, ip, project, spider_name):
        sd = ScrapydAPI(ip)
        return sd.schedule(project, spider_name)

    def stop_spider(self, ip, project, id):
        sd = ScrapydAPI(ip, project, id)
        return sd.cancel(project, id)


if __name__ == "__main__":
    temp = ScrapyBIL(SCRAPYD_API)
    print temp.deploy_spider("douban", "111", "../data/doubao.egg")
    print temp.scrapyd.list_projects()
    print temp.scrapyd.list_spiders("douban")
    print temp.scrapyd.list_jobs("douban")
    print temp.scrapyd.schedule("douban", "book")