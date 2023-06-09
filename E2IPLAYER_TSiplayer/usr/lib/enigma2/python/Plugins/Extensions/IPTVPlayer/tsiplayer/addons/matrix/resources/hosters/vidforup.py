#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler 
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import dialog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser 
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.xbmc import xbmcgui
import re
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidforup', 'vid4up')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
    
        sUrl = self._url
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
     # (.+?) ([^<]+)
        oParser = cParser()
        sPattern =  '<source src="([^<]+)" type=.+?res="([^<]+)">' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)
            stoken = ""
            stoken = api_call.split('token=')[1]

            if (api_call):
                return True,api_call+'|token='+stoken+ '&User-Agent=' + UA + '&Referer=https://blkom.com'  

        return False, False
