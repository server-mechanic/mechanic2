#!/bin/bash -e

source /build/integration-tests/testlib.sh

installMechanicViaBashInstaller

givenALocalMigration

/usr/local/bin/mechanic2 migrate

verifyLocalMigrationApplied
