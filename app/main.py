#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib

import tornado.ioloop
import tornado.web
from tornado.options import parse_command_line


class TornadoApp(tornado.web.Application):
    def __init__(self, env, cookie_secret):
        debug = True
        traceback = True

        if env != 'development':
            env = 'production'
            debug = False
            traceback = False

        template_path = str(pathlib.Path(__file__).parent.resolve() / env / 'template')
        static_path = str(pathlib.Path(__file__).parent.resolve() / env / 'static')

        settings = {
            'template_path': template_path,
            'static_path': static_path,
            'cookie_secret': cookie_secret,
            'xsrf_cookies': True,
            'debug': debug,
            'serve_traceback': traceback
        }

        handlers = [
            # (r'/', MainHandler),
        ]
        super().__init__(handlers, **settings)


if __name__ == '__main__':
    parse_command_line()
    env = os.environ['TORNADO_ENV']
    cookie_secret = os.environ['TORNADO_COOKIE_SECRET']
    TornadoApp(env).listen(int(os.environ['PORT']))
    tornado.ioloop.IOLoop.instance().start()
