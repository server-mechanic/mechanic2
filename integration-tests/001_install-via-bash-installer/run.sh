#!/bin/bash -e

source /build/integration-tests/testlib.sh

installMechanicViaBashInstaller

result=$(/usr/local/bin/mechanic2 version)

assertNotEmpty "version" "${result}"

