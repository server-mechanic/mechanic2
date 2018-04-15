#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import optparse

from mechanic2.exceptions import MechanicException
from mechanic2.env import MechanicEnv
from mechanic2.logger import logger

class MechanicConfig(object):
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
    optParser.add_option("-n", "--dry-run", action="store_true",
                  dest="dryRun", default=False,
                  help="apply no migrations, only simulate")
    optParser.add_option("-f", "--force", action="store_true",
                  dest="force", default=False,
                  help="force execution, ignore errors")
    optParser.add_option("-q", "--quiet", action="store_true",
                  dest="quiet", default=False,
                  help="don't print anything to stdout")
    optParser.add_option("-v", "--verbose", action="count",
                  dest="logLevel", default=0,
                  help="increase logging output")

    (options, args) = optParser.parse_args()
    logger.quiet = options.quiet
    logger.logLevel = logger.logLevel-options.logLevel
    self.force = options.force
    self.dryRun = options.dryRun
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
