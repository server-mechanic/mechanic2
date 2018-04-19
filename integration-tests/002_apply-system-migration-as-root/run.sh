#!/bin/bash -e

source /build/integration-tests/testlib.sh

installMechanicViaBashInstaller

givenASystemMigration

sudo /usr/local/bin/mechanic2 migrate

verifySystemMigrationApplied
