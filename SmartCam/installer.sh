#!/bin/sh
# ###########################################
# SCRIPT : DOWNLOAD AND INSTALL SmartCam
# ###########################################
#
# Command: wget https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/installer.sh -qO - | /bin/sh
#
# ###########################################

###########################################
# Configure where we can find things here #
TMPDIR='/tmp'
PACKAGE='enigma2-smartcam'
MY_URL='https://raw.githubusercontent.com/soomarali/Download/main/SmartCam'
URL_VER=''

#################
# Check Version #
#VERSION=$(wget $URL_VER/version -qO- | cut -d "=" -f2-)

####################
#  Image Checking  #

if [ -f /etc/opkg/opkg.conf ]; then
    OSTYPE='Opensource'
    OPKGINSTAL='opkg install'
    OPKGLIST='opkg list-installed'
    OPKGREMOV='opkg remove --force-depends'
elif [ -f /etc/apt/apt.conf ]; then
    OSTYPE='DreamOS'
    OPKGINSTAL='apt-get install'
    OPKGLIST='apt-get list-installed'
    OPKGREMOV='apt-get purge --auto-remove'
    DPKINSTALL='dpkg -i --force-overwrite'
#fi

##################################
# Remove previous files (if any) #
#rm -rf $TMPDIR/"${PACKAGE:?}"* >/dev/null 2>&1

######################
#  Remove Old Plugin #
#if [ "$($OPKGLIST $PACKAGE | awk '{ print $3 }')" = "$VERSION" ]; then
    echo " You are use the laste Version: $VERSION"
   # exit 1
#elif [ -z "$($OPKGLIST $PACKAGE | awk '{ print $3 }')" ]; then
#    echo
    clear
#else
    $OPKGREMOV $PACKAGE
#fi

###################
#  Install Plugin #
echo "SmartCam server plugin Please Wait ......"
if [ "$OSTYPE" = "Opensource" ]; then
    wget $MY_URL/${PACKAGE}_"${VERSION}"_all.ipk -qP $TMPDIR
    $OPKGINSTAL $TMPDIR/${PACKAGE}_"${VERSION}"_all.ipk
else
    wget $MY_URL/${PACKAGE}_"${VERSION}"_all.deb -qP $TMPDIR
    $DPKINSTALL $TMPDIR/${PACKAGE}_"${VERSION}"_all.deb
    $OPKGINSTAL -f -y
fi

#########################
# Remove files (if any) #
rm -rf $TMPDIR/"${PACKAGE:?}"*

sleep 1
clear
echo ""
echo "****************************************************************************************"
echo "**                                                                                     *"
echo "**                            SmartCam   : $VERSION                                    *"
echo "**                            Uploaded by: Asghar_Ai                                   *"
echo "**                                                                                     *"
echo "****************************************************************************************"
echo ""

if [ "$OSTYPE" = "Opensource" ]; then
    killall -9 enigma2
else
    systemctl restart enigma2
fi

exit 0

