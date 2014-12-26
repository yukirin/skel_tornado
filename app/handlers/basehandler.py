#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def initialize(self):
        pass

    def prepare(self):
        pass

    def on_finish(self):
        pass

    def set_cookie(*args, **kwargs):
        return super().set_cookie(*args, secure=True, httponly=True, **kwargs)

    def set_default_headers(self):
        self.add_header('X-Frame-Options', 'SAMEORIGIN')
        self.add_header('X-XSS-Protection', '1; mode=block')
        self.add_header('X-Content-Type-Options', 'nosniff')
        # self.add_header(
        #     'Strict-Transport-Security',
        #     'max-age=31536000; includeSubDomains'
        # )


class JSONBaseHandler(BaseHandler):
    render = BaseHandler.write
