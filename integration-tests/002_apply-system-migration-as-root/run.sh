#!/bin/bash -e

sudo /target/bash-installer-*.sh

cat - <<EOB | sudo bash
#!/bin/bash
mkdir -p /etc/mechanic2/migration.d/
echo -n "#!/bin/bash -e 
touch /marker
" > /etc/mechanic2/migration.d/001_touch_root.sh
chmod 755 /etc/mechanic2/migration.d/001_touch_root.sh
EOB

cat /etc/mechanic2/migration.d/001_touch_root.sh

sudo /usr/local/bin/mechanic2 migrate

if [ ! -f /marker ]; then
  exit 1
fi
