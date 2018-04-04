#!/usr/bin/env Python
# coding:utf-8
import os
from base_bil import BaseBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST
from DBaction.mongo_action import MongoAction
from DBaction.redis_action import RedisAction


class ScrapyBIL(BaseBIL):

    def __init__(self):
        super(ScrapyBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.redis_action = RedisAction()

    def insert_info(self, collection, info):
        self.mongo_action.insert(collection, info)

    def get_job_id(self):
        return self.redis_action.incr("schedule_job_id")

    def update_info(self, query, info, **kwargs):
        self.mongo_action.update("job_running", query, info, **kwargs)


if __name__ == "__main__":
    pass