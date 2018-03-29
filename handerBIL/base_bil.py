#!/usr/bin/env Python
# coding:utf-8


class AccountException(Exception):
    def __init__(self, err):
        super(AccountException, self).__init__(err)


class BaseBIL(object):

    def __init__(self):
        pass
