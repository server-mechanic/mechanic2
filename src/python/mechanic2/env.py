#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os

class MechanicEnv(object):
  def getRealUserHome(self):
    return os.path.expanduser("~{}".format(self.getRealUser()))

  def getRealUser(self):
    return os.environ['USER']

  def isRealUserRoot(self):
    return self.getRealUser() == "root"

  def isEffectiveUserRoot(self):
    return os.geteuid() == 0
