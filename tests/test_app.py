#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pathlib
from test.support import EnvironmentVarGuard

sys.path[0:0] = [str(pathlib.Path(__file__).parent.resolve() / '..' / 'app')]

from tornado.testing import AsyncHTTPTestCase, gen_test

from main import TornadoApp
from foremanenvparser import ForemanEnvParser


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
