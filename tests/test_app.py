#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main import TornadoApp
from tornado.testing import AsyncHTTPTestCase, gen_test


class TornadoAppTest(AsyncHTTPTestCase):
    def get_app(self):
        return TornadoApp()

    @gen_test
    def test_app(self):
        response = yield self.http_client.fetch(self.get_url('/'))
        self.assertEqual(str(response.body, 'utf-8'), "Hello, world")
