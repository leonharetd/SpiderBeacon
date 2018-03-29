#!/usr/bin/env Python
# coding:utf-8
from uuid import uuid4
import tornado.web
from base_handler import BaseHandler


class IndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        session = uuid4()
        self.render("index.html", session=session)


class Index2Handler(BaseHandler):

    def get(self):
        self.render('index2.html')

