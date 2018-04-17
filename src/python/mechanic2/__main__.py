#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import sys

from mechanic2.cli import MechanicCommand

if __name__ == "__main__":
  exitCode = MechanicCommand().run(sys.argv)
  sys.exit(exitCode)
