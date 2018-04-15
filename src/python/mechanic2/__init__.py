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

MECH2_VERSION=""

MECH2_SYSTEM_MIGRATION=0
MECH2_USER_MIGRATION=1
MECH2_LOCAL_MIGRATION=2

MECH2_DEBUG=0
MECH2_INFO=1
MECH2_WARNING=2
MECH2_ERROR=3

class Mech2Logger(object):
  def __init__(self, quiet=False):
    self.quiet = quiet
    self.logLevel = MECH2_INFO

  def debug(self, message, *args):
    self._log(MECH2_DEBUG, message, *args)

  def info(self, message, *args):
    self._log(MECH2_INFO, message, *args)

  def warn(self, message, *args):
    self._log(MECH2_WARNING, message, *args)

  def error(self, message, *args):
    self._log(MECH2_ERROR, message, *args)

  def _log(self, level, message, *args):
    if not self.quiet and level >= self.logLevel:
      print(message.format(*args))

logger = Mech2Logger()

class Mech2Migration(object):
  def __init__(self, file, name, type):
    self.file = file
    self.type = type
    self.name = name

  def isSystemMigration(self):
    return self.file == MECH2_SYSTEM_MIGRATION

  def isRootRequired(self):
    return self.isSystemMigration() or re.match("^.*as[_]?(root|admin)\\..*$", self.name.lower())

class Mech2MigrationCollector(object):
  def __init__self(object):
    pass

  def collectMigrations(self, env, config):
    migrations = []
    if env.isEffectiveUserRoot():
      self._collectMigrationsInto(migrations=migrations, dirs=config.systemMigrationDirs, type=MECH2_SYSTEM_MIGRATION)
    self._collectMigrationsInto(migrations=migrations, dirs=config.userMigrationDirs, type=MECH2_USER_MIGRATION)
    self._collectLocalMigrationsInto(migrations)
    migrations.sort(key=lambda m: m.name)
    return migrations

  def _collectLocalMigrationsInto(self, migrations):
    dir = os.getcwd()
    while dir != "/":
      migrationsDir = os.path.join(dir, ".mechanic2", "migration.d")
      if os.path.isdir(migrationsDir):
        self._collectMigrationsInto(migrations, [migrationsDir], MECH2_LOCAL_MIGRATION)
        return
      dir = os.path.dirname(dir)

  def _collectMigrationsInto(self, migrations, dirs, type):
    for dir in dirs:
      if os.path.isdir(dir):
        for file in os.listdir(dir):
          file = os.path.join(dir, file)
          if os.path.isfile(file):
             migration = Mech2Migration(file=file,name=os.path.basename(file),type=type)
             if not migration.file in [m.file for m in migrations]:
               migrations.append(migration)

class Mech2Config(object):
  def __init__(self, env, argv):
    self.userMigrationDirs = [ os.path.join(env.getRealUserHome(), ".mechanic2", "migration.d") ]
    self.systemMigrationDirs = [ "/etc/mechanic2/migration.d" ]
    self._parseOpts(argv)

    logger.debug("System migration dirs: {}", self.systemMigrationDirs)
    logger.debug("User migration dirs: {}", self.userMigrationDirs)
    logger.debug("Commands: {}", self.commands)
    logger.debug("Follow up command: {}", self.followUpCommand)

  def _parseOpts(self, argv):
    optParser = optparse.OptionParser(usage="usage: mechanic2 [options] migrate|version")
    optParser.add_option("-q", "--quiet", action="store_true",
                  dest="quiet", default=False,
                  help="don't print anything to stdout")
    optParser.add_option("-v", "--verbose", action="count",
                  dest="logLevel", default=0,
                  help="increase logging output")

    (options, args) = optParser.parse_args()
    logger.quiet = options.quiet
    logger.logLevel = logger.logLevel-options.logLevel
    self.commands = self._parseCommands(argv[1:], optParser)
    self.followUpCommand = self._parseFollowUpCommand(argv[1:])

    if len(self.commands) == 0:
      logger.error("Error: No command given!")
      optParser.print_help()
      raise MechanicException("")
    elif len(self.commands) > 1:
      logger.error("Error: Too many commands given!")
      optParser.print_help()
      raise MechanicException("")

  def _parseCommands(self, args, optParser):
    commands = []
    doubleDashSeen = False
    for arg in args:
      if not doubleDashSeen and arg == "--":
        doubleDashSeen = True
      elif not doubleDashSeen and not arg.startswith("-"):
        if not arg in ['migrate', 'version']:
          logger.error("Error: Unknown command: {}".format(arg))
          optParser.print_help()
          raise MechanicException("")
        commands.append(arg)
    return commands

  def _parseFollowUpCommand(self, args):
    followUpCommand = []
    doubleDashSeen = False
    for arg in args:
      if not doubleDashSeen and arg == "--":
        doubleDashSeen = True
      elif doubleDashSeen:
        followUpCommand.append(arg)
    return followUpCommand

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
    self.config = Mech2Config(env=self.env, argv=sys.argv)

  def run(self):
    for command in self.config.commands:
      if command == 'migrate':
        return self.migrate()
      elif command == 'version':
        return self.printVersion()
      else:
        raise MechanicException("Unknown command {}.".format(command))

  def printVersion(self):
    print("mechanic2 {}".format(MECH2_VERSION))
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

if __name__ == "__main__":
  exitCode = 1
  try:
    exitCode = Mech2Mechanic().run()
  except MechanicException as e:
    if e.message != "":
      logger.error("Error: {}".format(e.message))
  finally:
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(exitCode)
