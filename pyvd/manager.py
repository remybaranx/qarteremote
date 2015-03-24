# -*- coding: utf-8 -*-

import threading
import os
import urllib2
import pickle
import logging
import pyvd.parser
import parsers
import pyvd.updater
import pyvd.downloader
import pyvd.config

class Manager:

    """
        Handle all requests.  
    """

    #
    def __init__(self, p_configPath):
        self.systemConfig = pyvd.config.Config(p_configPath + "/system.json")
        self.userConfig   = pyvd.config.Config(p_configPath + "/user.json")
        self.updaters     = {}
        self.downloadList = {}

    #
    def start(self):
        self.createUpdaters()
        self.startUpdaters()
        
    #
    def stop(self):
        for key, updater in self.updaters.items():
            updater.stop()

    #
    def createDefaultSystemConfig(self):
        logging.info("create default system configuration")
        self.systemConfig["server.port"] =12345
        self.systemConfig.save()

        logging.info("configuration : %s", str(self.systemConfig))
        
    #
    def createDefaultUserConfig(self):
        logging.info("create default user configuration")
        logging.info("configuration : %s", str(self.userConfig))

    #
    def loadSystemConfig(self):
        logging.info("load system configuration")
        return self.systemConfig.load()
        
    #
    def loadUserConfig(self):
        logging.info("load user configuration")
        return self.userConfig.load()

    #
    def createUpdaters(self):
        logging.info("Creating updaters ...")
        for parserPlugin in pyvd.parser.Parser.plugins:
            parser  = parserPlugin()
            updater = pyvd.updater.Updater(parser, self.userConfig["updaters." + parser.id])
            self.updaters[parser.id] = updater
            logging.info(" -> %s (%s) loaded", parser.id, parser.name)

    #
    def startUpdaters(self):
        logging.info("Starting updaters ...")
        for key, updater in self.updaters.items():
            updater.start()
            updater.refresh()
            logging.info(" -> %s (%s) started", updater.parser.id, updater.parser.name)
    
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
            logging.error("Invalid channel Id %s", p_channelId)
            return False
            
        self.updaters[p_channelId].refresh()
        return True
            
    #
    def isChannelExists(self, p_channelId):
        return p_channelId in self.updaters.keys()
            
    #
    def getVideos(self, p_channelId):
        if not self.isChannelExists(p_channelId):
            logging.error("Invalid channel Id %s", p_channelId)
            return None

        return self.updaters[p_channelId].getVideos()

    #
    def getVideoInfo(self, p_channelId, p_videoId):
        if not self.isChannelExists(p_channelId):
            logging.error("Invalid channel Id %s", p_channelId)
            return None

        return self.updaters[p_channelId].getVideoInfo(p_videoId)
        
    #
    def getDownloadList(self):
        downloadList = []
        
        for key, item in self.downloadList.items():
            downloader = item["downloader"]
            
            if downloader is None:
                logging.warning("Skip %s item from the download list", key)
                continue
            
            downloadListItem = {}
            downloadListItem["channel"] = key.split("/")[0]
            downloadListItem["videoId"] = int(key.split("/")[-1])
            downloadListItem["downloadedSize"] = downloader.downloadedSize
            downloadListItem["totalSsize"] = downloader.totalSize
            downloadList.append(downloadListItem)
            
        return downloadList
        
    #
    def addToDownloadList(self, p_channelId, p_videoId, p_params = {}):
        
        # check channel ID
        if not self.isChannelExists(p_channelId):
            logging.error("Invalid channel Id %s", p_channelId)
            return False

        # check video ID
        videoInfo = self.updaters[p_channelId].getVideoInfo(p_videoId)
        
        if videoInfo is None:
            logging.error("Invalid video Id %d", p_videoId)
            return False

        # analyze parameters
        if not p_params.has_key("quality"):
            p_params["quality"] = "Low" # default quality : to move in a configuration file ?
            
        if not p_params.has_key("language"):
            p_params["language"] = self.systemConfig["language"]
        
        if not p_params.has_key("protocol"):
            p_params["protocol"]  = "HTTP" # default protocol : to move in a configuration file ?
        
        # prepare downloading
        url = videoInfo["streams"][p_params["protocol"]][p_params["language"]][p_params["quality"]]["url"]
        downloadDir = self.updaters[p_channelId].config["downloadDirectory"]
        
        # TODO: take date into account
        downloader = pyvd.downloader.HTTPDownloader(url, downloadDir)

        try:
            downloader.start()
        except:
            logging.error("Unable to start downloading %s", url)
            return False

        # add in the download list
        key = p_channelId + "/" + str(p_videoId)
        self.downloadList[key] = {}
        self.downloadList[key]["downloader"] = downloader
        self.downloadList[key]["params"] = p_params
      
        return True
    #
    def delFromDownloadList(self, p_channelId, p_videoId):
        # todo
        pass
    
