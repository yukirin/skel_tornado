#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib

from motor import MotorClient


def init_settings():
    env = os.environ['TORNADO_ENV']
    cookie_secret = os.environ['TORNADO_COOKIE_SECRET']
    version = os.environ['APP_VERSION']
    db = MotorClient(os.environ['MONGOHQ_URL']).rin_stg
    debug = True if env == 'development' else False

    template_path = str(pathlib.Path(__file__).parent.resolve() / env / 'dist' / 'template')
    static_path = str(pathlib.Path(__file__).parent.resolve() / env / 'dist' / 'static')

    return {
        'template_path': template_path,
        'static_path': static_path,
        'cookie_secret': cookie_secret,
        'xsrf_cookies': True,
        'debug': debug,
        'db': db,
        'version': version
    }
