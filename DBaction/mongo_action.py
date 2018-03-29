#!/usr/bin/env Python
# coding:utf-8
import pymongo
import traceback


class MongoAction(object):

    def __init__(self, host, port, db_name="SpiderBeacon"):
        self.db_name = db_name
        self.mongo_action = pymongo.MongoClient(host=host, port=port)
        print self.mongo_action[db_name].authenticate("SpiderBeacon", "1qazxcvfr432")

    def find(self, collection, query):
        try:
            db = self.mongo_action.get_database(self.db_name)
            collect = db.get_collection(collection)
            return collect.find(query)
        except Exception as e:
            print traceback.format_exc()

    def insert(self, collection, query):
        try:
            db = self.mongo_action.get_database(self.db_name)
            collect = db.get_collection(collection)
            collect.insert(query)
        except Exception as e:
            print traceback.format_exc()

    def update(self, collection, query, value, s_upsert=False, s_multi=False):
        try:
            db = self.mongo_action.get_database(self.db_name)
            collect = db.get_collection(collection)
            collect.update(query, value, upsert=s_upsert, multi=s_multi)
        except Exception as e:
            print traceback.format_exc()

    def save(self, collection, value):
        # 一次操作一条记录，根据‘_id’是否存在，决定插入或更新记录
        try:
            db = self.mongo_action.get_database(self.db_name)
            collect = db.get_collection(collection)
            collect.save(value)
        except Exception as e:
            print traceback.format_exc()


if __name__ == "__main__":
    temp = MongoAction("39.106.145.106", 27117)
    for i in temp.find("SpiderBeaconUser", {}):
        print i
