#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import re

class MechanicMigration(object):
  def __init__(self, file, name, systemMigration=False):
    self.file = file
    self.systemMigration = systemMigration
    self.name = name

  def isSystemMigration(self):
    return self.systemMigration == True

  def isRootRequired(self):
    return self.isSystemMigration() or re.match("^.*as[_]?(root|admin)\\..*$", self.name.lower())
