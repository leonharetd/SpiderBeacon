#!/usr/bin/env Python
# coding:utf-8
from uuid import uuid4
from handerBIL.login_bil import LoginBIL
from handerBIL.base_bil import AccountException
from base_handler import BaseHandler


class LoginHandler(BaseHandler):

    def get(self):
        session = uuid4()
        self.render("login.html", session=session)

    def post(self):
        login_bil = LoginBIL()
        user_name = self.get_argument("username", "")
        pass_word = self.get_argument("password", "")
        try:
            group, auth = login_bil.login_check(user_name, pass_word)
            self.set_secure_cookie("u", user_name)
            self.set_secure_cookie("g", group)
            self.set_secure_cookie("A", auth)
            self.redirect("/spider_dashboard")
        except AccountException as e:
            self.write(e.message)


class LogoutHandler(BaseHandler):

    def post(self):
        self.clear_all_cookies()
        self.redirect("/index")
