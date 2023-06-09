# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filepup', 'FilePup')

    def _getMediaLinkForGuest(self):
        oRequestHandler = cRequestHandler(self._url)
        # oRequestHandler.addParameters('login', '1')
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = 'type: "video\/mp4", *src: "([^<>"{}]+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            return True, aResult[1][0]

        return False, False
