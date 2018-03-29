#!/usr/bin/env Python
# coding:utf-8


class AccountException(Exception):
    def __init__(self, err):
        super(AccountException, self).__init__(err)


def auth_by_filter(jobs, group, user_name):
    auth_tag = map(lambda x: x["group"] == group and x["username"] in ["*", user_name], jobs)
    return zip(auth_tag, jobs)


class BaseBIL(object):

    def __init__(self):
        pass


