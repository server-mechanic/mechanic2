#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import sys
from mechanic2 import Mech2Mechanic, Mech2Exception

if __name__ == "__main__":
  exitCode = 1
  try:
    exitCode = Mech2Mechanic().run()
  except Mech2Exception as e:
    if e.message != "":
      print(e.message)
  finally:
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(exitCode)
