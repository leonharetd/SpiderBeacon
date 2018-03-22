#!/usr/bin/env Python
# coding:utf-8
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from handler.index_handler import IndexHandler, Index2Handler
from handler.login_handler import LoginHandler, LogoutHandler
from handler.cluster_manage_handler import ClusterManageHandler
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

routes = [
    (r"/index", IndexHandler),  # 来自根路径的请求用 IndesHandlers 处理
    (r"/login", LoginHandler),
    (r"/logout", LoginHandler),
    (r"/index2", Index2Handler),
    (r"/cluster_manage", ClusterManageHandler)
]


class Application(tornado.web.Application):
    def __init__(self):
        handlers = routes

        settings = {
            'template_path': 'templates',
            'static_path': 'static',
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "login_url": "/login"
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
