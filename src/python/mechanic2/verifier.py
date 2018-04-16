#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os

from mechanic2.exceptions import MechanicException
from mechanic2.env import MechanicEnv
from mechanic2.migration import MechanicMigration
from mechanic2.logger import logger
from mechanic2.config import MechanicConfig

class Verifier(object):
  def __init__(self, env, config):
    self.env = env
    self.config = config

  def verifyMigrations(self, migrations):
    valid = True
    for migration in migrations:
      if not os.access(migration.file, os.X_OK):
        logger.error("Error: {} ({}) is not executable.", migration.name, migration.file)
        valid = False
      if migration.isRootRequired() and not self.env.isEffectiveUserRoot():
        logger.error("Error: {} ({}) requires root/admin privileges.", migration.name, migration.file)
        valid = False
    return valid
