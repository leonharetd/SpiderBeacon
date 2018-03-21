#!/usr/bin/env Python
# coding:utf-8
from uuid import uuid4
from base_handler import BaseHandler


class LoginHandler(BaseHandler):

    def get(self):
        session = uuid4()
        self.render("login.html", session=session)

    def post(self):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/index")


class LogoutHandler(BaseHandler):

    def get(self):
        if self.get_argument("logout", None):
            self.clear_cookie("username")
            self.redirect("/")

    def post(self):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/index")
