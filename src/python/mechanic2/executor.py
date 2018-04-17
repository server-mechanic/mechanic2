#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import subprocess

from mechanic2.exceptions import MechanicException
from mechanic2.env import MechanicEnv
from mechanic2.migration import MechanicMigration
from mechanic2.logger import logger, noopLogger

class MigrationExecutor(object):
  def __init__(self, config):
    self.config = config

  def execute(self, migration, user=None, executeMigrations=True, printWhatWouldBe=noopLogger):
    if user is None:
      command = [migration.file]
    else:
      command = ["su", user, "-c", migration.file ]

    if executeMigrations:
      return self._executeMigration(migration, command)
    else:
      return self._simulateExecuteMigration(migration, command, printWhatWouldBe)

  def _executeMigration(self, migration, command):
    logger.debug("Running command: {}", command)
    migrationProcess = subprocess.Popen(command,bufsize=0,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=None,shell=False,cwd=os.path.dirname(migration.file))
    while True:
      line = migrationProcess.stdout.readline()
      if not line:
        break;
      logger.info("{}: {}", migration.name, line.strip())
    exitCode = migrationProcess.wait()
    return exitCode

  def _simulateExecuteMigration(self, migration, command, printWhatWouldBe=noopLogger):
    printWhatWouldBe.info("Would run command: {}", command)
    return 0
