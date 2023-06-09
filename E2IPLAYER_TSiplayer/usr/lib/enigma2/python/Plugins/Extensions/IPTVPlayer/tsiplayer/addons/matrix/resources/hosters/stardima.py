#-*- coding: utf-8 -*-

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import dialog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'stardima', 'stardima')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        
        oParser = cParser()
        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sHtmlContent = sHtmlContent.replace('\\', '')

        
            # (.+?) .+?
        sPattern = "size:'(.+?)',src:'(.+?)',"
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            url=[]
            qua=[]
            for i in aResult[1]:
                  url.append(str(i[1]))
                  qua.append(str(i[0])+"p")

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call
        return False, False
   
