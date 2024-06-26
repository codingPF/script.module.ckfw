# -*- coding: utf-8 -*-
"""
Kodi Interface

SPDX-License-Identifier: MIT
"""
import time
import xbmcplugin
import xbmcgui
import xbmc
import datetime
from . import utils as pyUtils

class KodiUI(object):

    ###########
    #
    ###########
    def __init__(self, pAddon, pContentType = 'video', pSortMethods = None, pCacheToDisc = False ):
        self.addon = pAddon
        self.logger = pAddon.createLogger('KodiUI')
        #
        self.allSortMethods = [
            xbmcplugin.SORT_METHOD_UNSORTED,
            xbmcplugin.SORT_METHOD_TITLE,
            xbmcplugin.SORT_METHOD_DATE,
            xbmcplugin.SORT_METHOD_DATEADDED,
            xbmcplugin.SORT_METHOD_DURATION
        ]
        if pSortMethods is not None:
            self.allSortMethods = pSortMethods
        #
        self.contentType = pContentType
        self.cacheToDisc = pCacheToDisc
        self.listItems = []
        self.startTime = 0
        self.tzBase = datetime.datetime.fromtimestamp(0)
        # just for documentation
        self.docuContentTypes = ['','video','movies']

    ######################################
    
    def addDirectories(self, pDataArray, pmode = None):
        self.logger.debug('addDirectory')
        for e in pDataArray:
            self.logger.debug('addDirectory {} : {} - {} - {} - {}', (pmode or e.mode), e.id, e.title, e.url, e.image)
            tgtUrl = self.addon.generateUrl({
                'mode': (pmode or e.mode),
                'urlB64': pyUtils.b64encode(e.url)
            })
            self.addDirectoryItem(pTitle = e.title, pUrl = tgtUrl, pIcon = e.image)

    def addItems(self, pDataArray, pmode = None):
        self.logger.debug('addItems')
        for e in pDataArray:
            self.logger.debug('addItems {} : {} - {} - {} - {} - {} - {} - {}', (pmode or e.mode), e.id, e.title, e.channel, e.aired, e.duration, e.image, e.url)
            tgtUrl = self.addon.generateUrl({
                'mode': (pmode or e.mode),
                'urlB64': pyUtils.b64encode(e.url)
            })
            self.addListItem(pTitle = e.title, pUrl = tgtUrl, pPlot = e.title, pDuration = e.duration, pAired = e.aired, pIcon = e.image)

    ######################################

    def addDirectoryItem(self, pTitle, pUrl, pSortTitle = None, pIcon = None, pContextMenu = None):
        self.addListItem(
            pTitle=pTitle, 
            pUrl=pUrl, 
            pSortTitle=None, 
            pPlot=None, 
            pDuration= None, 
            pAired= None, 
            pIcon=pIcon, 
            pContextMenu=pContextMenu,
            pPlayable='False',
            pFolder=True)

    def addListItem(self, pTitle, pUrl, pSortTitle = None, pPlot = None, pDuration = None, pAired = None, pIcon = None, pContextMenu = None, pPlayable = 'True', pFolder = False):
        #
        if self.startTime == 0:
            self.startTime = time.time()
        #
        if self.addon.getKodiVersion() > 17:
            listItem = xbmcgui.ListItem(label=pTitle, path=pUrl, offscreen=True)
        else:
            listItem = xbmcgui.ListItem(label=pTitle, path=pUrl)
        #
        if pPlayable == 'True':
            if self.addon.getKodiVersion() < 20:
                info_labels = {
                    'title': pTitle,
                    'sorttitle': pSortTitle if pSortTitle else pTitle.lower(),
                    'tvshowtitle': pTitle,
                    'plot': pPlot if pPlot else ''
                }
                #
                if pDuration:
                    info_labels['duration'] = '{:02d}:{:02d}:00'.format(*divmod(pDuration, 60))
                #
                if pAired:
                    if type(pAired) in (type(''), type(u'')):
                        ndate = pAired
                    else:
                        ndate = (self.tzBase + datetime.timedelta(seconds=(pAired))).isoformat()
                    airedstring = ndate.replace('T', ' ')
                    info_labels['date'] = airedstring[:10]
                    info_labels['aired'] = airedstring[:10]
                    info_labels['dateadded'] = airedstring
                    #
                    info_labels['plot'] = self.addon.localizeString(30101).format(airedstring) + info_labels['plot']
                    #
                # tpye is video to have plot and aired date etc.
                listItem.setInfo(type='video', infoLabels=info_labels)
            else:
                tag = listItem.getVideoInfoTag()
                tag.setTitle(pTitle)
                tag.setOriginalTitle(pTitle)
                tag.setSortTitle(pSortTitle if pSortTitle else pTitle.lower())
                tag.setTvShowTitle(pTitle)
                tag.setPlot(pPlot if pPlot else '')
                #
                if pDuration:
                    tag.setDuration(pDuration)
                #
                if pAired:
                    if type(pAired) in (type(''), type(u'')):
                        ndate = pAired
                    else:
                        ndate = (self.tzBase + datetime.timedelta(seconds=(pAired))).isoformat()
                    airedstring = ndate.replace('T', ' ')
                    tag.setDateAdded(airedstring) # (YYYY-MM-DD HH:MM:SS)
                    tag.setFirstAired(airedstring[:10])
                    tag.setLastPlayed(airedstring) #(YYYY-MM-DD HH:MM:SS)
                    tag.setPremiered(airedstring[:10])
                    tag.setYear(int(airedstring[:4]))
                    listItem.setDateTime(ndate) #YYYY-MM-DDThh:mm[TZD]
                    tag.setPlot(self.addon.localizeString(30101).format(airedstring) + (pPlot if pPlot else ''))
                    #
        #
        listItem.setProperty('IsPlayable', pPlayable)
        #
        if pIcon:
            listItem.setArt({
                'thumb': pIcon, #video 16:9 960w x 540h / Music 1:1 500w x 500h 
                'icon': pIcon, #16:9 640w x 360h 
                'banner': pIcon, #200:37 1000w x 185h 
                'fanart': pIcon, #16:9 1920w x 1080h
                'clearart': pIcon, # 16:9  1000w x 562h
                'clearlogo': pIcon # 80:31 800w x 310h 
            })
        #[('title1','action1'),('title2','action2'),...]
        if pContextMenu:
            listItem.addContextMenuItems(pContextMenu)
        #
        self.listItems.append((pUrl, listItem, pFolder))
        #

    # add aöö generated list items in one go
    def render(self):
        #
        for method in self.allSortMethods:
            xbmcplugin.addSortMethod(self.addon.getAddonHandle(), method)
        #
        xbmcplugin.setContent(self.addon.getAddonHandle(), self.contentType)
        #
        xbmcplugin.addDirectoryItems(
            handle=self.addon.getAddonHandle(),
            items=self.listItems,
            totalItems=len(self.listItems)
        )
        #
        xbmcplugin.endOfDirectory(self.addon.getAddonHandle(), cacheToDisc=self.cacheToDisc)
        #
        self.logger.debug('generated {} item(s) in {} sec', len(self.listItems), round(time.time() - self.startTime, 4))


