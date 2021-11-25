#!/bin/bash
# ###########################################
# SCRIPT : DOWNLOAD AND INSTALL TSIPlayer
# ###########################################
#
# Command: wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/IPTVPlayer/installer.sh -qO - | /bin/sh
#
# ###########################################

###########################################
# Configure where we can find things here #
VERSION='20.11.2021'
DUKTAPE='duktape'
PACKAGE='enigma2-plugin-extensions-e2iplayer-deps'
TMPDIR='/tmp'
CHECK=$(uname -m)
PLUGINPATH='/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer'
SETTINGS='/etc/enigma2/settings'
MY_URL='http://ipkinstall.ath.cx/ipk-install'

########################

if [ -f /etc/opkg/opkg.conf ] ; then
    STATUS='/var/lib/opkg/status'
    OSTYPE='Opensource'
    OPKG='opkg update'
    OPKGINSTAL='opkg install'
elif [ -f /etc/apt/apt.conf ] ; then
    STATUS='/var/lib/dpkg/status'
    OSTYPE='DreamOS'
    OPKG='apt-get update'
    OPKGINSTAL='apt-get install'
fi

if python --version 2>&1 | grep -q '^Python 3\.'; then
    echo ":You have Python3 image ..."
    PY3SQLITE='python3-sqlite3'
    PLUGINPY3='E2IPLAYER_TSiplayer-PYTHON3.tar.gz'
else
    echo ":You have Python2 image ..."
    PY2SQLITE='python-sqlite3'
    PLUGINPY2='E2IPLAYER_TSiplayer.tar.gz'
fi

#########################
# Remove files (if any) #
if python --version 2>&1 | grep -q '^Python 3\.'; then
    rm -rf ${TMPDIR}/"${PLUGINPY3:?}"
else
    rm -rf ${TMPDIR}/"${PLUGINPY2:?}"
fi

rm -rf ${PLUGINPATH}
rm -rf /etc/enigma2/iptvplaye*.json
rm -rf /etc/tsiplayer_xtream.conf
rm -rf /iptvplayer_rootfs
############################

$OPKG > /dev/null 2>&1
#####################
# Package Checking  #

if grep -qs "Package: $PACKAGE" $STATUS ; then
    echo ""
else
    if [ $OSTYPE = "Opensource" ]; then
        $OPKGINSTAL $PACKAGE
    else
        $OPKGINSTAL $PACKAGE
    fi
fi
################
if python --version 2>&1 | grep -q '^Python 3\.'; then
    if grep -qs "Package: $DUKTAPE" $STATUS ; then
        echo ""
    else
        echo "   >>>>   Need to install $DUKTAPE   <<<<"
        if [ $OSTYPE = "Opensource" ]; then
            echo " Downloading $DUKTAPE ......"
            $OPKGINSTAL $DUKTAPE
            clear
        fi
    fi
else
    if grep -qs "Package: $DUKTAPE" $STATUS ; then
        echo ""
    else
        echo "   >>>>   Need to install $DUKTAPE   <<<<"
        if [ $OSTYPE = "Opensource" ]; then
            echo " Downloading $DUKTAPE ......"
            $OPKGINSTAL $DUKTAPE
        elif [ $OSTYPE = "DreamOS" ]; then
            echo " Downloading $DUKTAPE ......"
            $OPKGINSTAL $DUKTAPE -y
        fi
    fi

fi
#################
if python --version 2>&1 | grep -q '^Python 3\.'; then
    if grep -qs "Package: $PY3SQLITE" $STATUS ; then
        echo
    else
        echo "   >>>>   Need to install $PY3SQLITE   <<<<"
        if [ $OSTYPE = "Opensource" ]; then
            echo " Downloading $PY3SQLITE ......"
            $OPKGINSTAL $PY3SQLITE
            clear
        fi
    fi
else
    if grep -qs "Package: $PY2SQLITE" $STATUS ; then
        echo
    else
        echo "   >>>>   Need to install $PY2SQLITE   <<<<"
        if [ $OSTYPE = "Opensource" ]; then
            echo " Downloading $PY2SQLITE ......"
            $OPKGINSTAL $PY2SQLITE
            clear
        fi
    fi

fi
################
sleep 1; clear
###############################
# Downlaod And Install Plugin #

if python --version 2>&1 | grep -q '^Python 3\.'; then
    set -e
    echo "Downloading And Insallling IPTVPlayer plugin Please Wait ......"
    echo
    wget $MY_URL/E2IPLAYER+TSIPLAYER-PYTHON3/$PLUGINPY3 -qP $TMPDIR
    tar -xzf $TMPDIR/$PLUGINPY3 -C /
    set +e
else
    set -e
    echo "Downloading And Insallling IPTVPlayer plugin Please Wait ......"
    echo
    wget $MY_URL/E2IPLAYER+TSIPLAYER/$PLUGINPY2 -qP $TMPDIR
    tar -xzf $TMPDIR/$PLUGINPY2 -C /
    set +e
fi

if [ "${CHECK}" = 'armv7l' ]; then
    plarform='armv7'
elif [ "${CHECK}" = 'mips' ]; then
    plarform='mipsel'
elif [ "${CHECK}" = 'aarch64' ]; then
    plarform='ARCH64'
elif [ "${CHECK}" = 'sh4' ]; then
    plarform='sh4'
fi

if [ -d $PLUGINPATH ]; then
    echo ":Your Device IS ${CHECK} processor ..."
    echo "Add Setting To ${SETTINGS} ..."
    init 4
    sleep 5
    sed -e s/config.plugins.iptvplayer.*//g -i ${SETTINGS}
    sleep 2
    {
        echo "config.plugins.iptvplayer.SciezkaCache=/etc/IPTVCache/"
        echo "config.plugins.iptvplayer.alternative${plarform^^}MoviePlayer=extgstplayer"
        echo "config.plugins.iptvplayer.alternative${plarform^^}MoviePlayer0=extgstplayer"
        echo "config.plugins.iptvplayer.buforowanie_m3u8=false"
        echo "config.plugins.iptvplayer.default${plarform^^}MoviePlayer=exteplayer"
        echo "config.plugins.iptvplayer.default${plarform^^}MoviePlayer0=exteplayer"
        echo "config.plugins.iptvplayer.remember_last_position=true"
        echo "config.plugins.iptvplayer.extplayer_infobanner_clockformat=24"
        echo "config.plugins.iptvplayer.extplayer_skin=halidri1080p1"
        echo "config.plugins.iptvplayer.plarform=${plarform}"
        echo "config.plugins.iptvplayer.dukpath=/usr/bin/duk"
        echo "config.plugins.iptvplayer.wgetpath=wget"
    } >> ${SETTINGS}
fi

#########################
# Remove files (if any) #
if python --version 2>&1 | grep -q '^Python 3\.'; then
    rm -rf ${TMPDIR}/"${PLUGINPY3:?}"
else
    rm -rf ${TMPDIR}/"${PLUGINPY2:?}"
fi

sync
echo ""
echo "***********************************************************************"
echo "**                                                                    *"
echo "**                       TSIPlayer  : $VERSION                      *"
echo "**                       Uploaded by: LINUXSAT                        *"
echo "**                       Script by  : MOHAMED_OS                      *"
echo "**                       Develop by : rgysoft                         *"
echo "**  Support    : https://www.tunisia-sat.com/forums/threads/3951696/  *"
echo "**                                                                    *"
echo "***********************************************************************"
echo ""

if which systemctl > /dev/null 2>&1; then
    sleep 2; systemctl restart enigma2
else
    init 4; sleep 2; init 3;
fi

exit 0
