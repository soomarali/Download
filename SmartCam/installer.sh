#!/bin/sh

# ==============================================
# SCRIPT : DOWNLOAD AND INSTALL SmartCam #
# =====================================================================================================================
# Command: wget https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/installer.sh -O - | /bin/sh #
# =====================================================================================================================

PACKAGE_DIR='soomarali/Download/main/SmartCam'
MY_IPK="enigma2-smartcam_11.572_all.ipk"

MY_MAIN_URL="https://raw.githubusercontent.com/soomarali/Download/main/SmartCam/"
if which opkg > /dev/null 2>&1; then
	MY_FILE=$MY_IPK
	MY_URL=$MY_MAIN_URL$PACKAGE_DIR'/'$MY_IPK
else
	echo
	echo ======================================
	echo == OPKG not found. Cannot continue. ==
	echo ======================================
	echo
	exit 1
fi
MY_TMP_FILE="/tmp/"$MY_FILE

echo ''
echo '****************************************************************************'
echo '**                                 STARTED                                **'
echo '****************************************************************************'
echo "**                            Uploaded by: ASGHAR_ALI                     **"
echo "**  https://www.tunisia-sat.com/forums/threads/4264626/#post-1055273465   **"
echo "****************************************************************************"
echo ''

rm -f $MY_TMP_FILE > /dev/null 2>&1

MY_SEP='============================================================='
echo $MY_SEP
echo 'Downloading '$MY_FILE' ...'
echo $MY_SEP
echo ''

wget -T 2 $MY_URL -P "/tmp/"

if [ -f $MY_TMP_FILE ]; then
	# Install
	echo ''
	echo $MY_SEP
	echo 'Installation started'
	echo $MY_SEP
	echo ''

	opkg install --force-reinstall $MY_TMP_FILE
	MY_RESULT=$?

	echo ''
	echo ''
	if [ $MY_RESULT -eq 0 ]; then
		echo "   >>>>   SUCCESSFULLY INSTALLED   <<<<"
		echo ''
		echo "   >>>>         RESTARING         <<<<"
		init 4; sleep 4; init 3;
	else
		echo "   >>>>   INSTALLATION FAILED !   <<<<"
	fi;
	echo ''
	echo '**************************************************'
	echo '**                   FINISHED                   **'
	echo '**************************************************'
	echo ''
	exit 0
else
	echo ''
	echo "Download failed !"
	exit 1
fi

# ------------------------------------------------------------------------------------------------------------
