#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import shutil
import subprocess
import re
import sys

from mechanic2.exceptions import MechanicException
from mechanic2.env import MechanicEnv
from mechanic2.migration import MechanicMigration
from mechanic2.logger import logger, noopLogger
from mechanic2.version import MECHANIC2_VERSION
from mechanic2.config import MechanicConfig
from mechanic2.executor import MigrationExecutor
from mechanic2.collector import MigrationCollector
from mechanic2.migrator import Migrator

def _raiseError(*kargs):
  raise MechanicException(message=kargs[0].format(kargs[1:]))

def _logError(*kargs):
  logger.error(*kargs)

class Mechanic(object):
  def __init__(self):
    self.env = MechanicEnv()
    self.config = MechanicConfig(env=self.env, argv=sys.argv)

  def run(self):
    for command in self.config.commands:
      if command == 'migrate':
        self.migrate()
      elif command == 'version':
        self.printVersion()
      else:
        raise MechanicException("Unknown command {}.".format(command))

  def printVersion(self):
    print("mechanic2 {}".format(MECHANIC2_VERSION))

  def migrate(self):
    migrations = self._collectMigrations()

    self._applyMigrations(migrations)

    if len(self.config.followUpCommand) > 0:
      exitCode = self._runFollowUpCommand(followUpCommand=self.config.followUpCommand, env=self.env)
      raise MechanicException("Follow up command exited with {}.", exitCode)

  def _collectMigrations(self):
    collector = MigrationCollector()
    migrations = collector.collectMigrations(env=self.env, config=self.config)
    return migrations

  def _applyMigrations(self, migrations):
    executor = MigrationExecutor(config=self.config)
    migrator = Migrator(env=self.env, executor=executor)
    if self.config.dryRun:
      printWhatWouldBe = logger
    else:
      printWhatWouldBe = noopLogger

    if self.config.force:
      handleError = _logError
    else:
      handleError = _raiseError

    migrator.applyMigrations(migrations, handleError=handleError,
                             executeMigrations=not self.config.dryRun, 
                             printWhatWouldBe=printWhatWouldBe)

  def _runFollowUpCommand(self, followUpCommand, env):
    try:
      if env.isEffectiveUserRoot() and not env.isRealUserRoot():
        followUpCommand2 = ['su', env.getRealUser(), '-c' ]
        followUpCommand2.extend(followUpCommand)
        if not self.config.dryRun:
          logger.debug("Running follow up command: {}", followUpCommand2)
          exitCode = os.execvpe(followUpCommand2[0], followUpCommand2, os.environ)
        else:
          logger.info("Would run follow up command: {}", followUpCommand2)
      else:
        if not self.config.dryRun:
          logger.debug("Running follow up command: {}", followUpCommand)
          exitCode = os.execvpe(followUpCommand[0], followUpCommand, os.environ)
        else:
          logger.info("Would run follow up command: {}", followUpCommand2)

      raise MechanicException("Running follow up command failed with {}.", exitCode)

    except Exception as e:
      raise MechanicException("Running follow up command failed with {}", e.message)
