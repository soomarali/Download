#!/bin/sh

# URL of the file to download
FILE_URL="https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/enigma2-smartcam_11.572_all.ipk"

# Destination path to save the downloaded file
DESTINATION="/var/tmp/"

# Download the file using wget
wget -O "/var/tmp/enigma2-smartcam_11.572_all.ipk" "https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/enigma2-smartcam_11.572_all.ipk"

opkg install "enigma2-smartcam_11.572_all.ipk"
# Check the download status
if [ $? -eq 0 ]; then
  echo "File downloaded successfully."
else
  echo "File download failed."
fi
# Install the IPK file
opkg install "enigma2-smartcam_11.572_all.ipk"

# Check the installation status
if [ $? -eq 0 ]; then
  echo "Package installed successfully."
else
  echo "Package installation failed."
fi
