#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# mechanic2 - see github.com/server-mechanic/mechanic2

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

class Mech2MigrationCollector(object):
  def __init__self(object):
    pass

  def collectMigrations(self, env, config):
    migrations = []
    if env.isEffectiveUserRoot():
      self._collectMigrationsInto(migrations=migrations, dirs=config.systemMigrationDirs, systemMigration=True)
    self._collectMigrationsInto(migrations=migrations, dirs=config.userMigrationDirs)
    self._collectLocalMigrationsInto(migrations)
    migrations.sort(key=lambda m: m.name)
    return migrations

  def _collectLocalMigrationsInto(self, migrations):
    dir = os.getcwd()
    while dir != "/":
      migrationsDir = os.path.join(dir, ".mechanic2", "migration.d")
      if os.path.isdir(migrationsDir):
        self._collectMigrationsInto(migrations, [migrationsDir])
        return
      dir = os.path.dirname(dir)

  def _collectMigrationsInto(self, migrations, dirs, systemMigration=False):
    for dir in dirs:
      if os.path.isdir(dir):
        for file in os.listdir(dir):
          file = os.path.join(dir, file)
          if os.path.isfile(file):
             migration = MechanicMigration(file=file,name=os.path.basename(file),systemMigration=systemMigration)
             if not migration.file in [m.file for m in migrations]:
               migrations.append(migration)

class Mech2MigrationExecutor(object):
  def __init__(self):
    pass

  def execute(self, migration, user=None):
    if user is None:
      command = [migration.file]
    else:
      command = ["su", user, "-c", migration.file ]

    logger.debug("Running command: {}", command)
    migrationProcess = subprocess.Popen(command,bufsize=0,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=None,shell=False,cwd=os.path.dirname(migration.file))
    while True:
      line = migrationProcess.stdout.readline()
      if not line:
        break;
      logger.info("{}: {}", migration.name, line.strip())
    exitCode = migrationProcess.wait()
    return exitCode

class Mech2MigrationVerifier(object):
  def __init__(self, env):
    self.env = env

  def verifyMigrations(self, migrations):
    valid = True
    for migration in migrations:
      if not os.access(migration.file, os.X_OK):
        logger.error("Error: {} ({}) is not executable.", migration.name, migration.file)
        valid = False
      if migration.isRootRequired() and not self.env.isEffectiveUserRoot():
        logger.error("Error: {} ({}) required root/admin privileges.", migration.name, migration.file)
        valid = False
    return valid

class Mech2Migrator(object):
  def __init__(self, env, executor):
    self.executor = executor
    self.env = env

  def applyMigrations(self, migrations):
    for migration in migrations:
      logger.info("Applying {}...", migration.name)
      if migration.isRootRequired() and not self.env.isEffectiveUserRoot():
        raise MechanicException("{} requires root.".format(migration.file))

      user = None
      if (not migration.isSystemMigration() 
        and not migration.isRootRequired()
        and self.env.isEffectiveUserRoot()
        and not self.env.isRealUserRoot()):
        user = self.env.getRealUser()
      exitCode = self.executor.execute(migration=migration, user=user)
      if exitCode != 0:
        logger.error("Error: {} failed.", migration.name)

class Mech2Mechanic(object):
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
    collector = Mech2MigrationCollector()
    migrations = collector.collectMigrations(env=self.env, config=self.config)
    verifier = Mech2MigrationVerifier(env=self.env)
    valid = verifier.verifyMigrations(migrations)
    if not valid:
      return 1
    executor = Mech2MigrationExecutor()
    migrator = Mech2Migrator(env=self.env, executor=executor)
    migrator.applyMigrations(migrations)

    exitCode = 0
    if len(self.config.followUpCommand) > 0:
      exitCode = self._runFollowUpCommand(followUpCommand=self.config.followUpCommand, env=self.env)
      raise MechanicException("Follow up command exited with {}.", exitCode)
      return 1

    return exitCode

  def _runFollowUpCommand(self, followUpCommand, env):
    try:
      if env.isEffectiveUserRoot() and not env.isRealUserRoot():
        followUpCommand2 = ['su', env.getRealUser(), '-c' ]
        followUpCommand2.extend(followUpCommand)
        logger.debug("Running follow up command: {}", followUpCommand2)
        exitCode = os.execvpe(followUpCommand2[0], followUpCommand2, os.environ)
      else:
        logger.debug("Running follow up command: {}", followUpCommand)
        exitCode = os.execvpe(followUpCommand[0], followUpCommand, os.environ)

      logger.error("Error: Running follow up command failed with {}.", exitCode)
      if exitCode != 0:
        return 1
      else:
        return 0
    except Exception as e:
      return 1
