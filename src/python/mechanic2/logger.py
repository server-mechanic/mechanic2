#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

LOG_LEVEL_DEBUG=0
LOG_LEVEL_INFO=1
LOG_LEVEL_WARNING=2
LOG_LEVEL_ERROR=3

class MechanicLogger(object):
  def __init__(self, quiet=False):
    self.quiet = quiet
    self.logLevel = LOG_LEVEL_INFO

  def debug(self, message, *args):
    self._log(LOG_LEVEL_DEBUG, message, *args)

  def info(self, message, *args):
    self._log(LOG_LEVEL_INFO, message, *args)

  def warn(self, message, *args):
    self._log(LOG_LEVEL_WARNING, message, *args)

  def error(self, message, *args):
    self._log(LOG_LEVEL_ERROR, message, *args)

  def _log(self, level, message, *args):
    if not self.quiet and level >= self.logLevel:
      print(message.format(*args))

logger = MechanicLogger()
