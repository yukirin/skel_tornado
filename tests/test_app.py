#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from test.support import EnvironmentVarGuard

from tornado.testing import AsyncHTTPTestCase, gen_test

from app.main import TornadoApp
from tests.foremanenvparser import ForemanEnvParser


class TornadoAppTest(AsyncHTTPTestCase):
    def get_app(self):
        with EnvironmentVarGuard() as env:
            config = ForemanEnvParser('.env')
            for env_var, value in config.env:
                env.set(env_var.upper(), value)
            return TornadoApp(os.environ['TORNADO_ENV'])

    @gen_test
    def test_app(self):
        response = yield self.http_client.fetch(self.get_url('/'))
        self.assertEqual(str(response.body, 'utf-8'), "Hello, world")
