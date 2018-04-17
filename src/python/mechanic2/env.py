#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import pwd

class MechanicEnv(object):
  def getRealUserHome(self):
    return os.path.expanduser("~{}".format(self.getRealUser()))

  def getRealUser(self):
    user = os.getenv("SUDO_USER")
    if user != None:
      return user

    user = os.getenv("LOGNAME")
    if user != None:
      return user

    user = os.getenv("USER")
    if user != None:
      return user

    user = pwd.getpwuid(os.getuid())[0]
    if user != None:
      return user

    raise MechanicException("Cannot determine real user name.")

  def isRealUserRoot(self):
    return self.getRealUser() == "root"

  def isEffectiveUserRoot(self):
    return os.geteuid() == 0
