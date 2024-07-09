#!/bin/bash
pip install latest-chromedriver
mkdir /chromedriver
# Download and install Chromedriver
wget -q --continue -P /chromedriver "https://storage.googleapis.com/chrome-for-testing-public/$(google-chrome --version | grep -o '[0-9.]\+')/linux64/chromedriver-linux64.zip"
unzip /chromedriver/chromedriver* -d /chromedriver
