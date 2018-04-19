#!/bin/bash -e

assertFileOwnerIs() {
  local file=$1
  local expectedOwner=$2

  local owner=$(stat -c '%U' "${file}")
  if [ "x${expectedOwner}" != "x${owner}" ]; then
    echo "Expected owner of ${file} to be ${expectedOwner}, but is ${owner}."
    exit 1
  fi
}

assertFileAbsent() {
  local file=$1
  if [ -e "$file" ]; then
    echo "Expected file/dir ${file} to be absent."
    exit 1
  fi 
}

assertFileExists() {
  local file=$1
  if [ ! -f "$file" ]; then
    echo "Expected file ${file} to exist."
    exit 1
  fi 
}

function assertNotEmpty() {
  local name="$1"
  local value="$2"
  if [ "x" = "x${value}" ]; then
    echo "Expected ${name} to be not empty."
    exit 1
  fi
}

function installMechanicViaBashInstaller() {
  sudo /build/target/bash-installer-*.sh
}

function givenASystemMigration() {
cat - <<EOB | sudo bash
#!/bin/bash
mkdir -p /etc/mechanic2/migration.d/
echo -n "#!/bin/bash -e
touch /marker
" > /etc/mechanic2/migration.d/001_touch_root.sh
chmod 755 /etc/mechanic2/migration.d/001_touch_root.sh
EOB

cat /etc/mechanic2/migration.d/001_touch_root.sh
}

givenARootUserMigration() {
# install root user migration
mkdir -p /root/.mechanic2/migration.d/

echo -n "#!/bin/bash -e
touch /root/marker
" > /root/.mechanic2/migration.d/005_touch_root_home_file.sh
chmod 755 /root/.mechanic2/migration.d/005_touch_root_home_file.sh

cat /root/.mechanic2/migration.d/005_touch_root_home_file.sh
}

givenAUserMigration() {
# install user migration
mkdir -p $HOME/.mechanic2/migration.d/

echo -n "#!/bin/bash -e
touch $HOME/marker
" > $HOME/.mechanic2/migration.d/002_touch_home_file.sh
chmod 755 $HOME/.mechanic2/migration.d/002_touch_home_file.sh

cat $HOME/.mechanic2/migration.d/002_touch_home_file.sh
}

givenALocalMigration() {
# install local migration 
LOCAL_DIR=$HOME/a/b/c
mkdir -p $LOCAL_DIR/.mechanic2/migration.d/

echo -n "#!/bin/bash -e
touch $HOME/marker.local
" > $LOCAL_DIR/.mechanic2/migration.d/003_touch_local_file.sh
chmod 755 $LOCAL_DIR/.mechanic2/migration.d/003_touch_local_file.sh

cd $LOCAL_DIR
}

function verifySystemMigrationApplied() {
  if [ ! -f "/marker" ]; then
    echo "System migration marker /marker missing."
    exit 1
  fi
}

function verifyUserMigrationApplied() {
  if [ ! -f "$HOME/marker" ]; then
    echo "User migration marker $HOME/marker missing."
    exit 1
  fi
}

function verifyRootUserMigrationApplied() {
  if [ ! -f "/root/marker" ]; then
    echo "Root user migration marker /root/marker missing."
    exit 1
  fi
}

function verifyLocalMigrationApplied() {
  if [ ! -f "$HOME/marker.local" ]; then
    echo "Local migration marker $HOME/marker.local missing."
    exit 1
  fi
}
