#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

from mechanic2.exceptions import MechanicException
from mechanic2.env import MechanicEnv
from mechanic2.migration import MechanicMigration
from mechanic2.logger import logger, noopLogger
from mechanic2.config import MechanicConfig
from mechanic2.executor import MigrationExecutor

class Migrator(object):
  def __init__(self, env, executor):
    self.executor = executor
    self.env = env

  def applyMigrations(self, migrations, handleError, executeMigrations=True, printWhatWouldBe=noopLogger):
    for migration in migrations:
      logger.info("Applying {}...", migration.name)
      self._verifyMigration(migration, handleError=handleError)

      user = None
      if (not migration.isSystemMigration() 
        and not migration.isRootRequired()
        and self.env.isEffectiveUserRoot()
        and not self.env.isRealUserRoot()):
        user = self.env.getRealUser()

      self.executor.execute(migration=migration, user=user, executeMigrations=executeMigrations, printWhatWouldBe=printWhatWouldBe, handleError=handleError)

  def _verifyMigration(self, migration, handleError):
    if migration.isRootRequired() and not self.env.isEffectiveUserRoot():
      handleError("Error: {} requires root.", migration.name)
