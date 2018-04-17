#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import sys

from mechanic2.exceptions import MechanicException
from mechanic2.mechanic import Mechanic

class MechanicCommand(object):
  def run(self, args):
    try:
      Mechanic().run()
      return 0
    except MechanicException as e:
      if e.message != "":
        print(e.message)
      else:
        traceback.print_exc()
      return 1
    except Error as e:
      traceback.print_exc()
      return 1
    finally:
      sys.stdout.flush()
      sys.stderr.flush()
