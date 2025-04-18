echo "Installing package"
sudo dpkg -i ${APP_NAME}-${APP_VERSION}.deb
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl start $APP_NAME