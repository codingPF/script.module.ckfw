# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
The logger module

"""
from . import utils as pyUtils
import xbmc


class Logger(object):

    def __init__(self, pPluginName, pVersion, pClass=None):
        self.name = pPluginName
        self.version = pVersion
        self.prefix = None
        self.set_topic(pClass)

    def getInstance(self, topic=None):
        """
        Generates a new logger instance with a specific topic

        Args:
            topic(str, optional): the topic of the new logger.
                Default is the same topic of `self`
        """
        return Logger(self.name, self.version, topic)

    def set_topic(self, topic=None):
        """
        Changes the topic of the logger

        Args:
            topic(str, optional): the new topic of the logger.
                If not specified or `None`, the logger will have
                no topic. Default is `None`
        """
        if topic is None:
            self.prefix = '[%s-%s]: ' % (self.name, self.version)
        else:
            self.prefix = '[%s-%s:%s]: ' % (self.name, self.version, topic)

    def debug(self, message, *args):
        """ Outputs a debug message """
        self._log(xbmc.LOGDEBUG, message, *args)

    def info(self, message, *args):
        """ Outputs an info message """
        self._log(xbmc.LOGINFO, message, *args)

    def warn(self, message, *args):
        """ Outputs a warning message """
        self._log(xbmc.LOGWARNING, message, *args)

    def error(self, message, *args):
        """ Outputs an error message """
        self._log(xbmc.LOGERROR, message, *args)

    def _log(self, level, message, *args):
        parts = []
        for arg in args:
            part = arg
            part = pyUtils.py2_encode(part)
            parts.append(part)
        message = pyUtils.py2_encode(message)
        xbmc.log(self.prefix + message.format(*parts), level=level)
