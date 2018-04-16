#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import sys

from mechanic2.exceptions import MechanicException
from mechanic2.mechanic import Mechanic

if __name__ == "__main__":
  exitCode = 1
  try:
    exitCode = Mechanic().run()
  except MechanicException as e:
    if e.message != "":
      print(e.message)
    else:
      traceback.print_exc()
  except Error as e:
    traceback.print_exc()
  finally:
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(exitCode)
