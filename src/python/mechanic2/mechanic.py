#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import shutil
import subprocess
import re
import sys
import optparse

from mechanic2.exceptions import MechanicException
from mechanic2.env import MechanicEnv
from mechanic2.migration import MechanicMigration
from mechanic2.logger import logger
from mechanic2.version import MECHANIC2_VERSION
from mechanic2.config import MechanicConfig
from mechanic2.executor import MigrationExecutor
from mechanic2.collector import MigrationCollector
from mechanic2.migrator import Migrator
from mechanic2.verifier import Verifier

class Mechanic(object):
  def __init__(self):
    self.env = MechanicEnv()
    self.config = MechanicConfig(env=self.env, argv=sys.argv)

  def run(self):
    for command in self.config.commands:
      if command == 'migrate':
        return self.migrate()
      elif command == 'version':
        return self.printVersion()
      else:
        raise MechanicException("Unknown command {}.".format(command))

  def printVersion(self):
    print("mechanic2 {}".format(MECHANIC2_VERSION))
    return 1

  def migrate(self):
    migrations = self._collectMigrations()

    valid = self._verifyMigrations(migrations)
    if not valid and not self.config.force:
      return 1

    self._applyMigrations(migrations)

    exitCode = 0
    if len(self.config.followUpCommand) > 0:
      exitCode = self._runFollowUpCommand(followUpCommand=self.config.followUpCommand, env=self.env)
      raise MechanicException("Follow up command exited with {}.", exitCode)

    return exitCode

  def _collectMigrations(self):
    collector = MigrationCollector()
    migrations = collector.collectMigrations(env=self.env, config=self.config)
    return migrations

  def _verifyMigrations(self, migrations):
    verifier = Verifier(env=self.env, config=self.config)
    valid = verifier.verifyMigrations(migrations)
    return valid

  def _applyMigrations(self, migrations):
    executor = MigrationExecutor(config=self.config)
    migrator = Migrator(env=self.env, config=self.config, executor=executor)
    migrator.applyMigrations(migrations)

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

      logger.error("Error: Running follow up command failed with {}.", exitCode)
      return 1
    except Exception as e:
      return 1
