#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 13:06
# @Author  : Fred Yang
# @File    : app.py
# @Role    : 启动程序


import fire
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
from tornado.options import define, options
from settings import settings as app_settings
from controller.app_mail import SendMailHandler


define("port", default=9001, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/sendmail', SendMailHandler)
        ]

        super(Application, self).__init__(handlers, **app_settings)
        # tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    fire.Fire(main)
