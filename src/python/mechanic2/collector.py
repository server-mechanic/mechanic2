#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os

from mechanic2.logger import logger
from mechanic2.migration import MechanicMigration
from mechanic2.config import MechanicConfig
from mechanic2.env import MechanicEnv
from mechanic2.migration_metadata_reader import MigrationMetadataReader

class MigrationCollector(object):
  def __init__(self):
    pass

  def collectMigrations(self, env, config):
    logger.debug("Collecting migrations...")
    migrations = []
    if env.isEffectiveUserRoot():
      logger.debug("Collecting system migrations...")
      self._collectMigrationsInto(migrations=migrations, dirs=config.systemMigrationDirs, systemMigration=True)

    logger.debug("Collecting user migrations...")
    self._collectMigrationsInto(migrations=migrations, dirs=config.userMigrationDirs)

    logger.debug("Collecting local migrations...")
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
    logger.debug("Collecting migrations from {}...", dirs)
    for dir in dirs:
      if os.path.isdir(dir):
        for file in os.listdir(dir):
          file = os.path.join(dir, file)
          if os.path.isfile(file):
             logger.debug("Found migration at {}...", file)
             metadata = MigrationMetadataReader(file).readMetadata()
             if metadata.get("mechanic-migration-repeatable", None) == None:
               logger.warn("No metadata present in {}. Default behaviour will change in next version, please add '# mechanic-migration-repeatable: true' to migration file to retain current behaviour.", file)

             migration = MechanicMigration(file=file,metadata=metadata,name=os.path.basename(file),systemMigration=systemMigration)
             if not migration.file in [m.file for m in migrations]:
               migrations.append(migration)
