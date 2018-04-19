#!/bin/bash -e

source /build/integration-tests/testlib.sh

installMechanicViaBashInstaller

givenAUserMigration

/usr/local/bin/mechanic2 migrate

verifyUserMigrationApplied
