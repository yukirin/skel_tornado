#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io

from configparser import SafeConfigParser


class FakeSecHead:
    def __init__(self, fp):
        self.config = io.StringIO()
        self.config.write('[dummy]\n')
        self.config.write(fp.read())
        self.config.seek(0, os.SEEK_SET)

    def __iter__(self):
        return self.config


class ForemanEnvParser:
    def __init__(self, file_name):
        config = SafeConfigParser()
        with open(file_name) as f:
            config.readfp(FakeSecHead(f))
        self.env = config.items('dummy')
