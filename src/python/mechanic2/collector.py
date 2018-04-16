#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os

from mechanic2.logger import logger

class MigrationCollector(object):
  def __init__(self):
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
