#!/usr/bin/env Python
# coding:utf-8
import os
from base_bil import BaseBIL
from DBaction.settings import MONGODB_PORT, MONGODB_HOST
from DBaction.mongo_action import MongoAction


class ScrapyBIL(BaseBIL):

    def __init__(self):
        super(ScrapyBIL, self).__init__()
        self.mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        self.upload_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    pass