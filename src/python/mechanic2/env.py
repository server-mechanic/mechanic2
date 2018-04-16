#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import getpass

class MechanicEnv(object):
  def getRealUserHome(self):
    return os.path.expanduser("~{}".format(self.getRealUser()))

  def getRealUser(self):
    user = os.getenv("SUDO_USER")
    if user != None:
      return user
    user = os.getenv("USER")
    if user != None:
      return user
    user = getpass.getuser()
    return user

  def isRealUserRoot(self):
    return self.getRealUser() == "root"

  def isEffectiveUserRoot(self):
    return os.geteuid() == 0
