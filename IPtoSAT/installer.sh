#!/bin/bash
# ###########################################
# SCRIPT : DOWNLOAD AND INSTALL IPtoSAT
# ###########################################
#
# Command: wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/IPtoSAT/installer.sh -qO - | /bin/sh
#
# ###########################################

###########################################
# Configure where we can find things here #
TMPDIR='/tmp'
MY_URL='https://raw.githubusercontent.com/MOHAMED19OS/Download/main/IPtoSAT'
pyVersion=$(python -c"from sys import version_info; print(version_info[0])")

#########################
if uname -n | grep -qs "^novaler4k" || uname -n | grep -qs "^multibox"; then
    VERSION='1.3-r0'
    PACKAGE='enigma2-plugin-extensions-ipsat'
    arrVar=("ffmpeg" "libc6" "enigma2-plugin-systemplugins-serviceapp" "exteplayer3" "gstplayer" "gstreamer1.0" "libglib-2.0-0")

    if [ "$pyVersion" = 3 ]; then
        arrVar+=("python3-cryptography" "python3-requests")
    else
        arrVar+=("python-core" "python-cryptography" "python-requests")
    fi
else
    VERSION='1.8'
    PACKAGE='enigma2-plugin-extensions-iptosat'
fi

#########################
if [ -f /etc/opkg/opkg.conf ]; then
    STATUS='/var/lib/opkg/status'
    OSTYPE='Opensource'
    OPKG='opkg update'
    OPKGINSTAL='opkg install'
    OPKGLIST='opkg list-installed'
    OPKGREMOV='opkg remove --force-depends'
elif [ -f /etc/apt/apt.conf ]; then
    STATUS='/var/lib/dpkg/status'
    OSTYPE='DreamOS'
    OPKG='apt-get update'
    OPKGINSTAL='apt-get install'
    OPKGLIST='apt-get list-installed'
    OPKGREMOV='apt-get purge --auto-remove'
    DPKINSTALL='dpkg -i --force-overwrite'
fi

#########################
install() {
    if grep -qs "Package: $1" "${STATUS}"; then
        echo
    else
        $OPKG >/dev/null 2>&1
        echo "   >>>>   Need to install $1   <<<<"
        echo
        if [ "${OSTYPE}" = "Opensource" ]; then
            $OPKGINSTAL "$1"
            sleep 1
            clear
        elif [ "${OSTYPE}" = "DreamOS" ]; then
            $OPKGINSTAL "$1" -y
            sleep 1
            clear
        fi
    fi
}

#########################
rm -rf $TMPDIR/"${PACKAGE:?}"* >/dev/null 2>&1

if [ "$($OPKGLIST $PACKAGE | awk '{ print $3 }')" = "$VERSION" ]; then
    echo " You are use the laste Version: $VERSION"
    exit 1
elif [ -z "$($OPKGLIST $PACKAGE | awk '{ print $3 }')" ]; then
    echo
    clear
else
    $OPKGREMOV $PACKAGE
fi

#########################
if uname -n | grep -qs "^novaler4k" || uname -n | grep -qs "^multibox"; then
    for i in "${arrVar[@]}"; do
        install "$i"
    done
else
    if [ "${OSTYPE}" = "Opensource" ]; then
        for i in exteplayer3 gstplayer; do
            install $i
        done
    elif [ "${OSTYPE}" = "DreamOS" ]; then
        install gstreamer1.0-plugins-base-apps
    fi
fi

#########################
echo "Insallling IPtoSAT plugin Please Wait ......"
if [ "${OSTYPE}" = "Opensource" ]; then
    wget $MY_URL/${PACKAGE}_"${VERSION}"_all.ipk -qP $TMPDIR
    $OPKGINSTAL $TMPDIR/${PACKAGE}_"${VERSION}"_all.ipk
else
    wget $MY_URL/${PACKAGE}_"${VERSION}".deb -qP $TMPDIR
    $DPKINSTALL $TMPDIR/${PACKAGE}_"${VERSION}".deb
    $OPKGINSTAL -f -y
fi

#########################
rm -rf $TMPDIR/"${PACKAGE:?}"*

sleep 1
clear
echo ""
echo "***********************************************************************"
echo "**                                                                    *"
echo "**                       IPtoSAT    : $VERSION                             *"
echo "**                       Uploaded by: MOHAMED_OS                      *"
echo "**                       Develop by : ZAKARIYA KHA                    *"
echo "**  Support    : https://www.tunisia-sat.com/forums/threads/4171372/  *"
echo "**                                                                    *"
echo "***********************************************************************"
echo ""

if [ "${OSTYPE}" = "Opensource" ]; then
    killall -9 enigma2
else
    systemctl restart enigma2
fi

exit 0
