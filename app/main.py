#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib

import tornado.ioloop
import tornado.web
from tornado.web import url
from tornado.options import parse_command_line
from motor import MotorClient


class TornadoApp(tornado.web.Application):
    def __init__(self, env):
        self.version = os.environ['APP_VERSION']
        db = MotorClient(os.environ['MONGOHQ_URL']).rin_stg
        debug = True

        if env != 'development':
            env = 'production'
            debug = False

        template_path = str(pathlib.Path(__file__).parent.resolve() / env / 'dist' / 'template')
        static_path = str(pathlib.Path(__file__).parent.resolve() / env / 'dist' / 'static')

        settings = {
            'template_path': template_path,
            'static_path': static_path,
            'cookie_secret': os.environ['TORNADO_COOKIE_SECRET'],
            'xsrf_cookies': True,
            'debug': debug,
            'db': db
        }

        handlers = [
            # url(r'/', MainHandler),
        ]
        super().__init__(handlers, **settings)


if __name__ == '__main__':
    parse_command_line()
    env = os.environ['TORNADO_ENV']
    TornadoApp(env).listen(int(os.environ['PORT']))
    tornado.ioloop.IOLoop.instance().start()
