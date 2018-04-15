#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

class MechanicException(Exception):
  def __init__(self, message, exitCode=1, printUsage=False):
    super(MechanicException, self).__init__(message)
    self.exitCode = exitCode
    self.printUsage = printUsage
