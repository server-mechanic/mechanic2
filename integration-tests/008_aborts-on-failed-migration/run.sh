#!/bin/bash

source /build/integration-tests/testlib.sh

installMechanicViaBashInstaller

givenAFailingUserMigration
givenAUserMigration

/usr/local/bin/mechanic2 migrate
exitCode=$?
assertEquals "exitCode" "1" "${exitCode}"

verifyUserMigrationNotApplied
