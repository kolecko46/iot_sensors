#!/bin/bash

if [[ -n "$SUDO_USER" ]]; then
    USER_HOME=$(eval echo ~$SUDO_USER)
else
    USER_HOME="$HOME"
fi

set -e  

# Name variables
APP_NAME="iotsensors"
APP_ROOT_FOLDER="$USER_HOME/debpkgs"

BUILD_FOLDER="${APP_ROOT_FOLDER}/${APP_NAME}"
DEBIAN_FOLDER="${BUILD_FOLDER}/DEBIAN"
INSTALL_FOLDER="${BUILD_FOLDER}/opt/${APP_NAME}"

# Create folder for git repository clone
REPO_FOLDER="${APP_ROOT_FOLDER}/repo"
GIT_URL="https://github.com/kolecko46/iot_sensors.git"


# 
sudo rm -rf /home/miro/debpkgs/iotsensors/opt/iotsensors/env/lib/python3.11/site-packages/matplotlib
# 


echo "Clean old build"
echo
rm -rf $APP_ROOT_FOLDER

echo "Install dependencies"
echo
sudo apt update && sudo apt install -y python3 python3-venv python3-pip dpkg-dev debhelper git libpq-dev python3-dev
echo
echo "Cloning repo"
git clone $GIT_URL $REPO_FOLDER
echo 

# Get commit ID
cd $REPO_FOLDER
GIT_COMMIT_ID=$(git rev-parse --short HEAD)
APP_DATE=$(date +"%Y%m%d")
APP_VERSION=${APP_DATE}-${GIT_COMMIT_ID}
cd

# Create folders
echo "Creating $DEBIAN_FOLDER and $INSTALL_FOLDER"
mkdir -p $DEBIAN_FOLDER
mkdir -p $INSTALL_FOLDER

# Move git content to install folder and delete repo_folder
echo "Moving git content to $INSTALL_FOLDER and deleting $REPO_FOLDER"
cp -r $REPO_FOLDER/* $INSTALL_FOLDER
rm -rf $REPO_FOLDER

# Create python virtual environment and install all dependencies
echo "Creating virtual environment"
python3 -m venv "$INSTALL_FOLDER/env"
echo "$INSTALL_FOLDER"
echo "env created"
$INSTALL_FOLDER/env/bin/pip install --upgrade pip
$INSTALL_FOLDER/env/bin/pip install -r $INSTALL_FOLDER/requirements.txt

# Create systemd service
echo "Creating systemd service"
mkdir -p $BUILD_FOLDER/etc/systemd/system
cat <<EOF | sudo tee $BUILD_FOLDER/etc/systemd/system/$APP_NAME.service
[Unit]
Description=IoT Sensors
After=network.target

[Service]
ExecStart=$INSTALL_FOLDER/env/bin/uvicorn main:app --host 0.0.0.0 --port 8000
WorkingDirectory=$INSTALL_FOLDER
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOF

# Create control file
echo $DEBIAN_FOLDER
touch $DEBIAN_FOLDER/control

cat <<EOF > $DEBIAN_FOLDER/control
Package: $APP_NAME
Version: $APP_VERSION
Architecture: all
Maintainer: Miro kolecani@gmail.com
Depends: python3, python3-venv, python3-pip
Section: web
Description: iot sensors
EOF

# Build .deb package
echo "Building .deb package"
dpkg-deb --build $BUILD_FOLDER ${APP_NAME}-${APP_VERSION}.deb

echo "Installing package"
sudo dpkg -i ${APP_NAME}-${APP_VERSION}.deb
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl start $APP_NAME