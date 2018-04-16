#!/bin/bash -e

sudo /target/bash-installer-*.sh

/usr/local/bin/mechanic2 version

sudo /usr/local/mechanic2/bin/uninstall.sh

if [ -f /usr/local/bin/mechanic2 ]; then
  exit 1
fi
