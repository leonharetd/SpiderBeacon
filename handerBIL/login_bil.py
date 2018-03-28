#!/usr/bin/env Python
# coding:utf-8
from base_bil import BaseBIL
from base_bil import AccountException
from DBaction.settings import MONGODB_PORT, MONGODB_HOST
from DBaction.mongo_action import MongoAction


class LoginBIL(BaseBIL):

    def __init__(self):
        super(LoginBIL, self).__init__()

    def login_check(self, user_name, pass_word):
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        user_info = mongo_action.find("user_info", {"username": user_name})
        if user_info:
            raise AccountException("account not exists")
        else:
            if pass_word != user_info["password"]:
                raise AccountException("Password Incorrect")
            return user_info["username"], user_info["group"], user_info["authority"]

    def register_check(self, user_name, pass_word, group, authority):
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        if mongo_action.find("user_info", {"username": user_name}):
            raise AccountException("account exists")
        else:
            user_info = {
                "username": user_name,
                "password": pass_word,
                "group": group,
                "authority": authority
            }
            mongo_action.insert("user_info", user_info)
