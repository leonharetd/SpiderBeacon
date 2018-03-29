#!/usr/bin/env Python
# coding:utf-8
import hashlib
import re
from base_bil import BaseBIL
from base_bil import AccountException
from DBaction.settings import MONGODB_PORT, MONGODB_HOST
from DBaction.mongo_action import MongoAction


class LoginBIL(BaseBIL):

    def __init__(self):
        super(LoginBIL, self).__init__()

    def login_check(self, user_name, pass_word):
        """
        登录检测, 帐号是否存在, 密码是否正确
        :param user_name: 用户名
        :param pass_word: 密码
        :return: 用户所在组, 用户权限
        """
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        user_info = mongo_action.find_one("user_info", {"username": user_name})
        if not user_info:
            raise AccountException("account not exists")
        else:
            if hashlib.md5(pass_word).hexdigest() != user_info["password"]:
                raise AccountException("Password Incorrect")
            return user_info["group"], str(user_info["authority"])

    def username_check(self, user_name):
        """
        检测username是否合法, 只能是数字和英文, 不能为敏感词
        :param user_name: 用户明
        :return: True or False
        """
        stop_word = {"delete", "remove", "shutdown", "rm"}
        if re.findall(re.compile(r"[^0-9a-zA-z]+"), user_name):
            return False
        elif filter(lambda x: user_name.startswith(x) or user_name.endswith(x), stop_word):
            return False
        return True

    def register_check(self, user_name, pass_word, group, authority):
        """
        注册检测, username是否符合注册条件
        :param user_name: 用户名
        :param pass_word: 密码
        :param group: 所在组
        :param authority: 权限等级0,1,2...
        :return: None
        """
        mongo_action = MongoAction(MONGODB_HOST, MONGODB_PORT)
        if mongo_action.find_one("user_info", {"username": user_name}):
            raise AccountException("account exists")
        else:
            if not self.username_check(user_name):
                raise AccountException("account illegal")

            user_info = {
                "username": user_name,
                "password": pass_word,
                "group": group,
                "authority": authority
            }
            mongo_action.insert("user_info", user_info)
