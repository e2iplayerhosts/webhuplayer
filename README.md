E2iPlayer Web HU Player host

Install:

~~~
wget --no-check-certificate https://github.com/e2iplayerhosts/webhuplayer/archive/master.zip -q -O /tmp/webhuplayer.zip
unzip -q -o /tmp/webhuplayer.zip -d /tmp
cp -r -f /tmp/webhuplayer-master/IPTVPlayer/* /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer
rm -r -f /tmp/webhuplayer*
~~~

restart enigma2 GUI
