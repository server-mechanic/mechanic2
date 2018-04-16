#!/bin/bash -e

sudo /target/bash-installer-*.sh

mkdir -p $HOME/.mechanic2/migration.d/

echo -n "#!/bin/bash -e
touch $HOME/marker
" > $HOME/.mechanic2/migration.d/001_touch_home_file.sh
chmod 755 $HOME/.mechanic2/migration.d/001_touch_home_file.sh

cat $HOME/.mechanic2/migration.d/001_touch_home_file.sh

/usr/local/bin/mechanic2 migrate

if [ ! -f $HOME/marker ]; then
  exit 1
fi
