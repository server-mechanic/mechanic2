#!/bin/bash -xe

sudo /target/bash-installer-*.sh

cat - <<EOB
mkdir -p /etc/mechanic2/migration.d/
echo -n '#!/bin/bash -x\ntouch /marker' > /etc/mechanic2/migration.d/001_touch_root.sh
chmod 755 /etc/mechanic2/migration.d/001_touch_root.sh
EOB | sudo bash

sudo /usr/local/bin/mechanic2 migrate

if [ ! -f /marker ]; then
  exit 1
fi
