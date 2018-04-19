#!/bin/bash -ex

source /build/integration-tests/testlib.sh

installMechanicViaBashInstaller

mkdir -p $HOME/.mechanic2/migration.d/

givenAUserMigration

sudo /usr/local/bin/mechanic2 migrate

assertFileExists "$HOME/marker"
assertFileOwnerIs "$HOME/marker" build

