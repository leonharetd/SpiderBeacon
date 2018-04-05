#!/usr/bin/env Python
# coding:utf-8


class AccountException(Exception):
    def __init__(self, err):
        super(AccountException, self).__init__(err)


def get_auth(func):
    def wrapper(self, **kwargs):
        jobs = list(func(self, **kwargs))
        auth_tag = map(lambda x: x["group"] in kwargs["group"] and x["username"] in ["*", kwargs["username"]], jobs)
        return zip(auth_tag, jobs)
    return wrapper


def filter_with_group(func):
    def wrapper(self, **kwargs):
        jobs = list(func(self, **kwargs))
        new_jobs = filter(lambda x: x["group"] in kwargs["group"], jobs)
        return new_jobs
    return wrapper


def filter_with_username(func):
    def wrapper(self, **kwargs):
        jobs = list(func(self, **kwargs))
        new_jobs = filter(lambda x: x["username"] in ["*", kwargs["username"]], jobs)
        return new_jobs
    return wrapper


def filter_with_creator_group(func):
    def wrapper(self, creator):
        jobs = list(func(self, creator))
        news_jobs = filter(lambda x: x["group"] == x["username"], jobs)
        return news_jobs
    return wrapper


class BaseBIL(object):

    def __init__(self):
        pass


