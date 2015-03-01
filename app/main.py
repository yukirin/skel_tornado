#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import tornado.ioloop
import tornado.web
from tornado.web import url
from tornado.options import parse_command_line

import settings


class TornadoApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            # url(r'/', MainHandler),
        ]
        app_settings = settings.init_settings()
        super().__init__(handlers, **app_settings)


if __name__ == '__main__':
    parse_command_line()
    TornadoApp().listen(int(os.environ['PORT']))
    tornado.ioloop.IOLoop.instance().start()
