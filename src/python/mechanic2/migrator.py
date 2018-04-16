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
  def __init__(self, env, executor):
    self.executor = executor
    self.env = env

  def verifyMigration(self, migration, ignoreErrors=False):
    if migration.isRootRequired() and not self.env.isEffectiveUserRoot():
      if ignoreErrors:
        logger.error("Error: {} requires root.", migration.name)
      else:
        raise MechanicException("Error: {} requires root.".format(migration.name))

  def applyMigrations(self, migrations, ignoreErrors=False, executeMigrations=True, printWhatWouldBe=False):
    for migration in migrations:
      logger.info("Applying {}...", migration.name)
      self.verifyMigration(migration, ignoreErrors=ignoreErrors)

      user = None
      if (not migration.isSystemMigration() 
        and not migration.isRootRequired()
        and self.env.isEffectiveUserRoot()
        and not self.env.isRealUserRoot()):
        user = self.env.getRealUser()

      exitCode = self.executor.execute(migration=migration, user=user, executeMigrations=executeMigrations, printWhatWouldBe=printWhatWouldBe)
      if exitCode != 0:
        if ignoreErrors:
          logger.error("Error: {} failed.", migration.name)
        else:
          raise MechanicException("Error: {} failed.".format(migration.name))
