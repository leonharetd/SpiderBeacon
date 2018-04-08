# encoding: utf-8
import sys
import redis
import json
import hashlib
import random
from settings import REDIS_HOST, REDIS_PORT, PASS_WD
reload(sys)
sys.setdefaultencoding('utf8')


class RedisAction(object):

    def __init__(self, db=0):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=PASS_WD, db=db)

    def incr(self, key):
        return self.redis.incr(key)

    def rpush(self, name, value):
        return self.redis.rpush(name, value)

    def get_list(self, name):
        return self.redis.lrange(name, 0, -1)

    def queue_delete(self, name):
        return self.redis.delete(name)


if __name__ == "__main__":
    # temp = RedisAction()
    temp = RedisAction()
    print temp.rpush("test1", json.dumps((1, 2)))
    for i in temp.get_list("test1"):
        print json.loads(i)[1]
    # print temp.priority_queue_pop("page_list_task", 1)
    pass
