﻿# -*- coding: utf-8 -*-
###################################################
# 2019-04-19 by Alec - WebHUPlayer
###################################################
HOST_VERSION = "1.0"
###################################################
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.components.ihost import CHostBase, CBaseHostClass, CDisplayListItem, RetHost, CUrlItem
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import  printDBG, GetLogoDir
from Plugins.Extensions.IPTVPlayer.tools.iptvfilehost import IPTVFileHost
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper import getDirectM3U8Playlist, getF4MLinksWithMeta, getMPDLinksWithMeta
from Plugins.Extensions.IPTVPlayer.libs.urlparser import urlparser
from Plugins.Extensions.IPTVPlayer.libs import ph
###################################################

###################################################
# FOREIGN import
###################################################
from Components.config import config, ConfigYesNo, ConfigDirectory, getConfigListEntry
from os.path import normpath
from Tools.Directories import resolveFilename, fileExists, SCOPE_PLUGINS
###################################################

###################################################
# Config options for HOST
###################################################
config.plugins.iptvplayer.webhuplayer_dir = ConfigText(default = "/hdd", fixed_size = False)

def GetConfigList():
    optionList = []
    optionList.append(getConfigListEntry("Web HU Player könyvtár:", config.plugins.iptvplayer.webhuplayer_dir))
    return optionList
###################################################

def gettytul():
    return 'Web HU Player'

class webhuplayer(CBaseHostClass):

    def __init__(self):
        printDBG("webhuplayer.__init__")
        CBaseHostClass.__init__(self)
        path = config.plugins.iptvplayer.webhuplayer_dir + '/'
        self.currFileHost = None

    def _getHostingName(self, url):
        if 0 != self.up.checkHostSupport(url):
            return self.up.getHostName(url)
        elif self._uriIsValid(url):
            return (_('direct link'))
        else:
            return (_('unknown'))

    def _uriIsValid(self, url):
        return '://' in url
        
    def listMainMenu(self, cItem):
        try:
            msg_host = 'Webes tartalmak'
            MAIN_CAT_TAB = [{'category': 'list_main', 'title': 'Webes tartalmak', 'tab_id': 'webes', 'desc': msg_webes}
                           ]
            self.listsTab(MAIN_CAT_TAB, cItem)
        except Exception:
            printExc()
            
    def listMainItems(self, cItem):
        try:
            tabID = cItem.get('tab_id', '')
            if tabID == 'webes':
                self.Webes_tartalmak(cItem)
            else:
                return
        except Exception:
            printExc()

    def listSecondItems(self, cItem):
        try:
            tabID = cItem.get('tab_id', '')
        except Exception:
            printExc()            
            
    def Webes_tartalmak(self, cItem):
        msg = 'Jelenleg nem üzemel ez a fúnkció! Nemsokára működni fog.'
        self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
        return
                
    def getLinksForVideo(self, cItem):
        printDBG("Urllist.getLinksForVideo url[%s]" % cItem['url'])
        videoUrls = []
        uri = urlparser.decorateParamsFromUrl(cItem['url'])
        protocol = uri.meta.get('iptv_proto', '')
        
        printDBG("PROTOCOL [%s] " % protocol)
        
        urlSupport = self.up.checkHostSupport( uri )
        if 1 == urlSupport:
            retTab = self.up.getVideoLinkExt( uri )
            videoUrls.extend(retTab)
        elif 0 == urlSupport and self._uriIsValid(uri):
            if protocol == 'm3u8':
                retTab = getDirectM3U8Playlist(uri, checkExt=False, checkContent=True)
                videoUrls.extend(retTab)
            elif protocol == 'f4m':
                retTab = getF4MLinksWithMeta(uri)
                videoUrls.extend(retTab)
            elif protocol == 'mpd':
                retTab = getMPDLinksWithMeta(uri, False)
                videoUrls.extend(retTab)
            else:
                videoUrls.append({'name':'direct link', 'url':uri})
        return videoUrls
    
    def handleService(self, index, refresh = 0, searchPattern = '', searchType = ''):
        printDBG('handleService start')
        CBaseHostClass.handleService(self, index, refresh, searchPattern, searchType)
        name     = self.currItem.get("name", '')
        category = self.currItem.get("category", '')
        printDBG( "handleService: |||||||||||||||||||||||||||||||||||| name[%s], category[%s] " % (name, category) )
        self.currList = []
        if name == None:
            self.listMainMenu( {'name':'category'} )
        elif category == 'list_main':
            self.listMainItems(self.currItem)
        elif category == 'list_second':
            self.listSecondItems(self.currItem)
        else:
            printExc()
        CBaseHostClass.endHandleService(self, index, refresh)

class IPTVHost(CHostBase):

    def __init__(self):
        CHostBase.__init__(self, webhuplayer(), True, [])