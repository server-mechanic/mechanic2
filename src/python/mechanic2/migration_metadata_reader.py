#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from mechanic2.logger import logger
import re

class MigrationMetadataReader(object):
  def __init__(self, path):
    self.path = path

  def readMetadata(self):
    metadata = {}
    with open(self.path, "r") as file:
      while True:
        line = file.readline()
        if not line:
          break

        line = line.rstrip()

        match = re.match('^\s*#\s*(mechanic-[A-Za-z0-9\-]+):\s*([^\s]+)\s*$', line)
        if match != None:
          key = match.group(1)
          value = self.coerce(match.group(2))
          metadata[key] = value

    logger.debug("Metadata of {}: {}", self.path, metadata)
    return metadata

  def coerce(self, value):
    if value.lower() == 'true':
      return True
    if value.lower() == 'false':
      return False

    match = re.match("^\s*(\d+)\s*$", value)
    if match != None:
      return int(match.group(1))

    match = re.match("^\s*\"([^\"]+)\"\s*", value)
    if match != None:
      return match.group(1)

    match = re.match("^\s*'([^']+)'\s*", value)
    if match != None:
      return match.group(1)

    return value
