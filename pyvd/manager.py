# -*- coding: utf-8 -*-

import threading
import os
import urllib2
import pickle
import pyvd.parser
import parsers
import pyvd.updater
import pyvd.downloader

class Manager:

    """
        Handle all requests.  
    """

    def __init__(self):
        self.userConfig   = {}
        self.systemConfig = {}
        self.updaters     = {}
        self.downloadList = {}

    def start(self):
        self.createUpdaters()
        self.startUpdaters()
        
    def stop(self):
        for key, updater in self.updaters.items():
            updater.stop()

    def loadConfig(self):
        if not self.loadSystemConfig():
            return False
            
        return self.loadUserConfig()

    def loadSystemConfig(self):
        # to do
        return True
        
    def loadUserConfig(self):
        # to move in a configuration file
        self.userConfig["UPDATERS"] = {}
        self.userConfig["UPDATERS"]["arteplus"] = {'refreshPeriod' : 15}
        return True

    def createUpdaters(self):
        for parserPlugin in pyvd.parser.Parser.plugins:
            parser  = parserPlugin()
            updater = pyvd.updater.Updater(parser, self.userConfig["UPDATERS"][parser.id])
            self.updaters[parser.id] = updater

    def startUpdaters(self):
        for key, updater in self.updaters.items():
            updater.start()
            updater.refresh()

    #------------------
    # API manager
    #------------------

    #
    def getChannels(self):
        channelList = []
        for key, item in self.updaters.items():
            channelList.append({"id": item.parser.id, "name": item.parser.name})
            
        return channelList

    #
    def refreshChannel(self, p_channelId):
        if not self.isChannelExists(p_channelId):
            print "Invalid channel Id {}".format(p_channelId)
            return False
            
        self.updaters[p_channelId].refresh()
        return True
            
    #
    def isChannelExists(self, p_channelId):
        return p_channelId in self.updaters.keys()
            
    #
    def getVideos(self, p_channelId):
        if not self.isChannelExists(p_channelId):
            print "Invalid channel Id {}".format(p_channelId)
            return None

        return self.updaters[p_channelId].getVideos()

    #
    def getVideoInfo(self, p_channelId, p_videoId):
        if not self.isChannelExists(p_channelId):
            print "Invalid channel Id {}".format(p_channelId)
            return None

        return self.updaters[p_channelId].getVideoInfo(p_videoId)
        
    #
    def getDownloadList(self):
        downloadList = []
        
        for key, item in self.downloadList.items():
            downloadListItem = {}
            downloadListItem["channel"] = key.split("/")[0]
            downloadListItem["videoId"] = int(key.split("/")[-1])
            downloadListItem["downloadedSize"] = item["downloadedSize"]
            downloadListItem["totalSsize"] = item["totalSsize"]
            downloadList.append(downloadListItem)
            
        return downloadList
        
    #
    def addToDownloadList(self, p_channelId, p_videoId):
        
        # check channel ID
        if not self.isChannelExists(p_channelId):
            print "Invalid channel Id {}".format(p_channelId)
            return False

        # check video ID
        videoInfo = self.updaters[p_channelId].getVideoInfo(p_videoId)
        
        if videoInfo is None:
            print "Invalid video Id {}".format(p_videoId)
            return False
        
        # prepare downloading
        # TODO: modify to take into account HTTP/RTMP selection, quality, date, ...
        downloader = pyvd.downloader.HTTPDownloader(videoInfo["streams"]["HTTP"]["fr"]["Low"]["url"], "/tmp")

        try:
            downloader.start()
        except:
            print "Unable to start downloading {}".format(videoInfo["streams"]["HTTP"]["fr"]["Low"]["url"])
            return False

        # add in the download list
        key = p_channelId + "/" + str(p_videoId)
        self.downloadList[key] = {}
        self.downloadList[key]["downloadedSize"] = -1
        self.downloadList[key]["totalSsize"] = -1
        self.downloadList[key]["downloader"] = downloader
        self.downloadList[key]["params"] = None
      
        return True
    #
    def delFromDownloadList(self, p_channelId, p_videoId):
        pass
    
