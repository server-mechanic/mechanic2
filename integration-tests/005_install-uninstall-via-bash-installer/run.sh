#!/bin/bash -e

source /build/integration-tests/testlib.sh

installMechanicViaBashInstaller

result=$(/usr/local/bin/mechanic2 version)

assertNotEmpty "version" "${result}"

sudo /usr/local/mechanic2/bin/uninstall.sh

assertFileAbsent "/usr/local/bin/mechanic2"
assertFileAbsent "/usr/local/mechanic2"
