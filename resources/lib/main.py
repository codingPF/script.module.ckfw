# -*- coding: utf-8 -*-
"""
The main addon module

SPDX-License-Identifier: MIT

"""
from resources.lib.fw.kodi import Kodi
from resources.lib.fw.kodiUi import KodiUI
import resources.lib.fw.utils as pyUtils


#
class Main(Kodi):

    def __init__(self):
        super(Main, self).__init__()
        self.logger = self.createLogger('MAIN')
        #

    def run(self):
        #
        mode = self.getParameters('mode')
        parameterId = self.getParameters('id')
        self.logger.info('Run Plugin with Parameters {}', self.getParameters())
        if mode == 'something':
            tgtUrl = pyUtils.b64decode(self.getParameters('urlB64'))
            self.logger.debug('target url {}', tgtUrl)
            self._generateSomething(tgtUrl)
        elif mode == 'play':
            tgtUrl = pyUtils.b64decode(self.getParameters('urlB64'))
            self.logger.info('Play Url {}', tgtUrl)
            self.playItem(tgtUrl)
            #
        else:
            self._generateRoot()

        #

    # General
    def someSetting(self):
        return self.getSetting('someSetting') == 'true'

    
    # Processors
    
    # generate all ARD episodes from news
    def _generateRoot(self):
        self.logger.debug('_generateArdFolder')
        dataArray = []
        dataArray.extend(None)
        ui = KodiUI(self)
        ui.addItems(dataArray,'someSetting')
        ui.render()

    # generate all episodes for a ZDF show
    def _generateSomething(self, pUrl):
        self.logger.debug('_generateZdfEntity')
        dataArray = []
        dataArray.extend(None)
        ui = KodiUI(self)
        ui.addItems(dataArray, 'play')
        ui.render()
    
