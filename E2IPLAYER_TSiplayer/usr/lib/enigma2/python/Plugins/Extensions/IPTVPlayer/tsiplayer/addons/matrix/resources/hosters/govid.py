from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import dialog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog

UA = 'Android'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'govid', 'CimaClub', 'gold')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if '/down/'  in sUrl:
            self._url = self._url.replace("/2down/","/play/").replace("/down/","/play/")

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = ""
        surl = self._url.split('|Referer=')[0]
        sReferer = self._url.split('|Referer=')[1]

        oRequest = cRequestHandler(surl)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()
        oParser = cParser()

       # (.+?) .+? ([^<]+)
        sPattern =  '<small>([^<]+)</small> <a target="_blank" download=.+?href="([^<]+)">' 
        aResult = oParser.parse(sHtmlContent,sPattern)  
        if aResult[0]:
            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + surl

        return False, False
