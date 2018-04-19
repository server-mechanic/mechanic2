#!/bin/bash -e

source /build/integration-tests/testlib.sh

installMechanicViaBashInstaller

givenASystemMigration
givenAUserMigration
givenALocalMigration

sudo /usr/local/bin/mechanic2 migrate

verifySystemMigrationApplied
verifyUserMigrationApplied
verifyLocalMigrationApplied
