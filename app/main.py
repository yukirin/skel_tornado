#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import binascii
import pathlib

import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.escape import to_unicode


class TornadoApp(tornado.web.Application):
    def __init__(self):
        settings = {
            'template_path': str(pathlib.Path(__file__).parent.resolve() / 'template'),
            'static_path': str(pathlib.Path(__file__).parent.resolve() / 'static'),
            'cookie_secret': to_unicode(binascii.hexlify(os.urandom(64))),
            'xsrf_cookies': True,
            # debug option
            'debug': True,
            'serve_traceback': True,
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
    TornadoApp().listen(int(os.environ['PORT']))
    tornado.ioloop.IOLoop.instance().start()
