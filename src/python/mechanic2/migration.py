#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

class MechanicMigration(object):
  def __init__(self, file, name, metadata, systemMigration=False, rootRequired=False):
    self.file = file
    self.systemMigration = systemMigration
    self.name = name
    self.metadata = metadata
    self.rootRequired = rootRequired

  def isSystemMigration(self):
    return self.systemMigration == True

  def isRootRequired(self):
    return self.isSystemMigration() or self.rootRequired == True
