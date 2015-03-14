# -*- coding: utf-8 -*-

import threading
import os
import urllib2
import pickle
import pyvd.channel
import channels
import pyvd.updater
import pyvd.downloader

class Manager:

    """
        Handle all requests.  
    """

    def __init__(self):
        self.channels     = {}
        self.userConfig   = {}
        self.systemConfig = {}
        self.updater    = pyvd.updater.Updater(self)
        self.downloader = pyvd.downloader.Downloader(self)

    def start(self):
        self.loadChannels()
        
    def stop(self):
        pass
        
    def loadConfig(self):
        if not self.loadSystemConfig():
            return False
            
        return self.loadUserConfig()

    def loadSystemConfig(self):
        return True
        
    def loadUserConfig(self):
        return True

    def loadChannels(self):
        for channelPlugin in pyvd.channel.Channel.plugins:
            channel = channelPlugin()
            self.channels[channel.id] = channel

    def getChannels(self):
        channelList = []
        for key, item in self.channels.items():
            channelList.append({"id": item.id, "name": item.name})
            
        return channelList

    def refreshChannel(self, p_channelId):
        #todo
        pass

    def getVideos(self, p_channelId):
        #todo
        pass

    def getVideoInfo(self, p_videoId):
        #todo
        pass
        
    def addVideoToDownloadList(self, p_videoId):
        pass
        
    def removeVideoFromDownloadList(self, p_videoId):
        pass
    
