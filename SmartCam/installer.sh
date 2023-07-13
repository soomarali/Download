#!/bin/sh

# ###########################################
# SCRIPT : DOWNLOAD AND INSTALL OSCAM SMARTCAM
# ###########################################
#
# Command: wget https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/installer.sh -qO - | /bin/sh
#
# ###########################################
# URL of the file to download
FILE_URL="https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/enigma2-smartcam_11546_all.ipk"

# Destination path to save the downloaded file
DESTINATION="/var/tmp/"

# Download the file using wget
wget -O "/var/tmp/enigma2-smartcam_11546_all.ipk" "https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/enigma2-smartcam_11546_all.ipk"

opkg install /var/tmp/enigma2-smartcam_11546_all.ipk
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
echo ""
echo "***********************************************************************"
echo "**                                                                    *"
echo "**                       SmartCam     : v4                            *"
echo "**                       Uploaded by: ASGHAR_ALI                      *"
echo "**                       Develop For : DREAMWORLD                     *"
echo "**                       Support     : 03357300604                    *"
echo "**                                                                    *"
echo "***********************************************************************"
echo ""

exit 0
