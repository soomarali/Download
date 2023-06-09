#!/bin/sh
cp $1/iptvupdate/custom/xxx.sh $2/iptvupdate/custom/xxx.sh
status=$?
if [ $status -ne 0 ]; then
	echo "Błąd krytyczny. Plik $0 nie może zostać skopiowany, error[$status]."
	exit 1
fi
cp $1/hosts/hostXXX.py $2/hosts/
cp $1/icons/logos/XXXlogo.png $2/icons/logos/
cp $1/icons/PlayerSelector/XXX*.png $2/icons/PlayerSelector/ 
status=$?
if [ $status -ne 0 ]; then
	echo "Uwaga, Nie udało się skopiować XXX, error[$status]."
else
	echo "Kopiowanie XXX OK"
fi
if [ -x /usr/bin/fullwget ] ; then
	/usr/bin/fullwget --no-check-certificate http://www.blindspot.nhely.hu/hosts/hostxxx.tar.gz -q -O /tmp/iptv-host-xxx.tar.gz
else
	wget --no-check-certificate https://www.blindspot.nhely.hu/hosts/hostxxx.tar.gz -q -O /tmp/iptv-host-xxx.tar.gz
fi
	if [ -s /tmp/iptv-host-xxx.tar.gz ] ; then
		tar -xzf /tmp/iptv-host-xxx.tar.gz -C /tmp 
		cp -r -f /tmp/iptv-host-xxx-master*/IPTVPlayer/icons/PlayerSelector/* $2/icons/PlayerSelector/
		cp -r -f /tmp/iptv-host-xxx-master*/IPTVPlayer/icons/logos/* $2/icons/logos/
		cp -r -f /tmp/iptv-host-xxx-master*/IPTVPlayer/iptvupdate/custom/* $2/iptvupdate/custom/
		cp -r -f /tmp/iptv-host-xxx-master*/IPTVPlayer/hosts/* $2/hosts/
		rm -r -f /tmp/iptv-host-xxx*
		if [ -e $2/icons/PlayerSelector/XXX100 ] ; then
			mv $2/icons/PlayerSelector/XXX100 $2/icons/PlayerSelector/XXX100.png
			mv $2/icons/PlayerSelector/XXX120 $2/icons/PlayerSelector/XXX120.png
			mv $2/icons/PlayerSelector/XXX135 $2/icons/PlayerSelector/XXX135.png
			echo "Rename file png OK"
		fi
		echo "Download XXX tar.gz OK"
	else
		echo "Uwaga, Nie udał się Download XXX tar.gz"
	fi
echo "Wykonywanie $0 zakończone sukcesem."
exit 0
