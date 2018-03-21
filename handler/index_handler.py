#!/usr/bin/env Python
# coding:utf-8
from uuid import uuid4
import tornado.web
from base_handler import BaseHandler


class IndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)


