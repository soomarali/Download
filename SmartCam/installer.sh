#!/bin/sh

# URL of the file to download
FILE_URL="https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/enigma2-smartcam_11.572_all.ipk"

# Destination path to save the downloaded file
DESTINATION="/var/tmp/"

# Download the file using wget
wget -O "enigma2-smartcam_11.572_all.ipk" "https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/enigma2-smartcam_11.572_all.ipk"

# Check the download status
if [ $? -eq 0 ]; then
  echo "File downloaded successfully."
else
  echo "File download failed."
fi
