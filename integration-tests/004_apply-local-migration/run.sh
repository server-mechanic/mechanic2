#!/bin/bash -e

sudo /target/bash-installer-*.sh

LOCAL_DIR=$HOME/a/b/c

mkdir -p $LOCAL_DIR/.mechanic2/migration.d/

echo -n "#!/bin/bash -e
touch $HOME/marker
" > $LOCAL_DIR/.mechanic2/migration.d/001_touch_home_file.sh
chmod 755 $LOCAL_DIR/.mechanic2/migration.d/001_touch_home_file.sh

cd $LOCAL_DIR

/usr/local/bin/mechanic2 migrate

if [ ! -f $HOME/marker ]; then
  exit 1
fi
