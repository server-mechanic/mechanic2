#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

from mechanic2.exceptions import MechanicException
from mechanic2.env import MechanicEnv
from mechanic2.migration import MechanicMigration
from mechanic2.logger import logger
from mechanic2.config import MechanicConfig
from mechanic2.executor import MigrationExecutor

class Migrator(object):
  def __init__(self, env, config, executor):
    self.executor = executor
    self.env = env
    self.config = config

  def applyMigrations(self, migrations):
    for migration in migrations:
      logger.info("Applying {}...", migration.name)
      if migration.isRootRequired() and not self.env.isEffectiveUserRoot():
        if self.config.force:
          logger.error("Error: {} requires root.", migration.name)
        else:
          raise MechanicException("{} requires root.".format(migration.name))

      user = None
      if (not migration.isSystemMigration() 
        and not migration.isRootRequired()
        and self.env.isEffectiveUserRoot()
        and not self.env.isRealUserRoot()):
        user = self.env.getRealUser()
      exitCode = self.executor.execute(migration=migration, user=user)
      if exitCode != 0:
        if self.config.force:
          logger.error("Error: {} failed.", migration.name)
        else:
          raise MechanicException("{} failed.".format(migration.name))
