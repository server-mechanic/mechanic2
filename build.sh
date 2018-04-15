#!/bin/bash

PROJECT_DIR=$(cd `dirname $0` && pwd)

source ${PROJECT_DIR}/buildrc

SRC_DIR=${PROJECT_DIR}/src
BUILD_DIR=${PROJECT_DIR}/target
BUNDLE_BUILD_DIR=${BUILD_DIR}/bundle

function clean() {
  rm -rf ${BUILD_DIR}
}

function copyFiles() {
  mkdir -p ${BUNDLE_BUILD_DIR}/usr/local/bin ${BUNDLE_BUILD_DIR}/usr/local/mechanic2/lib/ ${BUNDLE_BUILD_DIR}/usr/local/mechanic2/bin/
  cp -r ${SRC_DIR}/python/* ${BUNDLE_BUILD_DIR}/usr/local/mechanic2/lib/
  perl -i -pe "s#MECH2_VERSION=\"\"#MECH2_VERSION=\"${LONG_VERSION}\"#g" ${BUNDLE_BUILD_DIR}/usr/local/mechanic2/lib/mechanic2/__init__.py
  touch ${BUNDLE_BUILD_DIR}/usr/local/mechanic2/bin/uninstall.sh
  cp ${SRC_DIR}/bash/mechanic2 ${BUNDLE_BUILD_DIR}/usr/local/mechanic2/bin/
  ln -s ../mechanic2/bin/mechanic2 ${BUNDLE_BUILD_DIR}/usr/local/bin/mechanic2
  find ${BUNDLE_BUILD_DIR} -type d -print0 | xargs -0 chmod 755
  find ${BUNDLE_BUILD_DIR} -type f -print0 | xargs -0 chmod 644
  chmod 755 ${BUNDLE_BUILD_DIR}/usr/local/mechanic2/bin/uninstall.sh
  chmod 755 ${BUNDLE_BUILD_DIR}/usr/local/mechanic2/bin/mechanic2
}

function createArchive() {
  cd ${BUNDLE_BUILD_DIR} && \
	tar czf ${BUILD_DIR}/bundle.tgz --absolute-names --owner=root:0 --group=root:0 usr
}

function createPackages() {
  ${PROJECT_DIR}/packaging/bash-installer/build.sh ${VERSION}
}

clean
copyFiles
createArchive
createPackages
