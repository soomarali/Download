# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.gui.hoster import cHosterGui

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'allow_redirects', 'Allow_redirects')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        oRequestHandler = cRequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()

        if sHosterUrl == self._url:
            return False, False

        elif sHosterUrl:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            oHoster.setUrl(sHosterUrl)
            api_call = oHoster.getMediaLink()

            if api_call[0]:
                return True, api_call[1]

        else:
            return False, False

        return False, False
