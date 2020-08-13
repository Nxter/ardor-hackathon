# -*- coding: UTF-8 -*-

import logging
import json
import sys

from datetime import datetime
from sigbro_ac import version
from sigbro_ac import application

logger = logging.getLogger()


class sigbroLogs:
    APP = None

    def __init__(self):
        self.APP = application

    def info(self, msg, **kwargs):
        tmp = {}
        tmp["timestamp"] = str(datetime.utcnow()) + " UTC"
        tmp["version"] = version
        tmp["application"] = self.APP
        tmp["level"] = "info"

        tmp["msg"] = msg

        try:
            if kwargs is not None:
                for key, value in kwargs.items():
                    tmp[key] = str(value)
        except:
            pass

        try:
            logger.warning(json.dumps(tmp))
        except:
            print("---- INFO ----------------------")
            print(tmp)
            print("----- E N D ----------------")

    def error(self, msg, **kwargs):
        tmp = {}
        tmp["timestamp"] = str(datetime.utcnow()) + " UTC"
        tmp["version"] = version
        tmp["application"] = self.APP
        tmp["level"] = "error"

        tmp["msg"] = msg

        try:
            if kwargs is not None:
                for key, value in kwargs.items():
                    tmp[key] = str(value)
        except:
            pass

        try:
            logger.warning(json.dumps(tmp))
        except:
            print("---- ERROR ----------------------")
            print(tmp)
            print("----- E N D ----------------")

    def warning(self, msg, **kwargs):
        tmp = {}
        tmp["timestamp"] = str(datetime.utcnow()) + " UTC"
        tmp["version"] = version
        tmp["application"] = self.APP
        tmp["level"] = "warning"

        tmp["msg"] = msg

        try:
            if kwargs is not None:
                for key, value in kwargs.items():
                    tmp[key] = str(value)
        except:
            pass

        try:
            logger.warning(json.dumps(tmp))
        except:
            print("---- WARNING ----------------------")
            print(tmp)
            print("----- E N D ----------------")

    def debug(self, msg, **kwargs):
        tmp = {}
        tmp["timestamp"] = str(datetime.utcnow()) + " UTC"
        tmp["version"] = version
        tmp["application"] = self.APP
        tmp["level"] = "debug"

        tmp["msg"] = msg

        try:
            if kwargs is not None:
                for key, value in kwargs.items():
                    tmp[key] = str(value)
        except:
            pass

        try:
            logger.warning(json.dumps(tmp))
        except:
            print("---- DEBUG ----------------------")
            print(tmp)
            print("----- E N D ----------------")
