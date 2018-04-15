#!/bin/bash

PROJECT_DIR=$(cd `dirname $0`/../.. && pwd)
PACKAGE_VERSION=$1
if [ "x" = "x${PACKAGE_VERSION}" ]; then
  echo "No PACKAGE_VERSION defined."
  exit 1
fi

BUILD_DIR=${PROJECT_DIR}/target/
PACKAGE_BUILD_DIR=${BUILD_DIR}/bash-installer
PACKAGE_FILE=${BUILD_DIR}/bash-installer-${PACKAGE_VERSION}.sh
PACKAGE_SRC_DIR=${PROJECT_DIR}/packaging/bash-installer/src

rm -rf ${PACKAGE_BUILD_DIR} && mkdir -p ${PACKAGE_BUILD_DIR}

echo "Building bash installer..."
(while read line; do
  if [[ "BUNDLE_DATA_HERE" = "$line" ]]; then
    cat ${BUILD_DIR}/bundle.tgz | base64
  else
    echo $line
  fi
done)>${PACKAGE_FILE} <${PACKAGE_SRC_DIR}/installer.sh.template
chmod 755 ${PACKAGE_FILE}

exit 0
