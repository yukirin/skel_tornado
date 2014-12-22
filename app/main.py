#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import binascii
import pathlib

import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.escape import to_unicode
from tornado.options import parse_command_line


class TornadoApp(tornado.web.Application):
    def __init__(self, env):
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
            'cookie_secret': to_unicode(binascii.hexlify(os.urandom(64))),
            'xsrf_cookies': True,
            'debug': debug,
            'serve_traceback': traceback
        }

        handlers = [
            (r'/', MainHandler),
        ]
        super().__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, page="1"):
        self.render("index.html")

    def render(self, *args, **kwargs):
        self.add_header('X-Content-Type-Options', 'nosniff')
        super().render(*args, **kwargs)

if __name__ == '__main__':
    parse_command_line()
    env = os.environ['TORNADO_ENV']
    TornadoApp(env).listen(int(os.environ['PORT']))
    tornado.ioloop.IOLoop.instance().start()
