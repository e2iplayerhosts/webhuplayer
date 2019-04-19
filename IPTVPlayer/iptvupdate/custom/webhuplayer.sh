#!/bin/sh
echo "webhuplayer.sh: start"
cp $1/iptvupdate/custom/webhuplayer.sh $2/iptvupdate/custom/webhuplayer.sh
status=$?
if [ $status -ne 0 ]; then
	echo "webhuplayer.sh: Critical error. The $0 file can not be copied, error[$status]."
	exit 1
fi
cp $1/hosts/hostwebhuplayer.py $2/hosts/
hosterr=$?
cp $1/icons/logos/webhuplayerlogo.png $2/icons/logos/
logoerr=$?
cp $1/icons/PlayerSelector/webhuplayer*.png $2/icons/PlayerSelector/
iconerr=$?
if [ $hosterr -ne 0 ] || [ $logoerr -ne 0 ] || [ $iconerr -ne 0 ]; then
	echo "webhuplayer.sh: copy error from source hosterr[$hosterr], logoerr[$logoerr, iconerr[$iconerr]"
fi
wget --no-check-certificate https://github.com/e2iplayerhosts/webhuplayer/archive/master.zip -q -O /tmp/webhuplayer.zip
if [ -s /tmp/webhuplayer.zip ] ; then
	unzip -q -o /tmp/webhuplayer.zip -d /tmp
	cp -r -f /tmp/webhuplayer-master/IPTVPlayer/hosts/hostwebhuplayer.py $2/hosts/
	hosterr=$?
	cp -r -f /tmp/webhuplayer-master/IPTVPlayer/icons/* $2/icons/
	iconerr=$?
	if [ $hosterr -ne 0 ] || [ $iconerr -ne 0 ]; then
		echo "webhuplayer.sh: copy error from webhuplayer-master hosterr[$hosterr], iconerr[$iconerr]"
	fi
else
	echo "webhuplayer.sh: webhuplayer.zip could not be downloaded."
fi
rm -r -f /tmp/webhuplayer*
echo "webhuplayer.sh: exit 0"
exit 0