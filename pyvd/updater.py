# -*- coding: utf-8 -*-

import threading
import copy
import logging
import pyvd.parser
import os
import urllib2

#
class Updater(threading.Thread):
    
    def __init__(self, p_parser, p_config):
        threading.Thread.__init__(self)
        self.parser = p_parser
        self.config = p_config
        self.videos = []
        self.refreshEvent  = threading.Event()
        self.mutex         = threading.RLock()
        self.isRunning     = False
        
    def run(self):

        logging.info("start updater for %s (%s)", self.parser.id, self.parser.name)

        # sanity checks
        if self.parser is None:
            logging.error("Invalid parser")
            return False

        # main update loop
        self.isRunning = True
        
        while self.isRunning:

            logging.debug("wait for refresh event [period=%d]", self.config["refreshPeriod"])

            # wait for a refresh event (or until the refresh period is elapsed)
            self.refreshEvent.wait(self.config["refreshPeriod"])

            if not self.isRunning:
                continue

            # start refreshing the video list
            logging.debug("start refreshing video list for %s (%s) ...", self.parser.id, self.parser.name)

            videos = self.parser.parse()

            # update the videos list
            with self.mutex:
                logging.debug("update video list")
                self.videos = videos

            # get thumbnails if required
            if self.config["downloadThumbnails"]:
                logging.debug("downloading thumbnails for %s (%s) ...", self.parser.id, self.parser.name)

                for i in range(0, len(videos)):

                    logging.debug("downloading thumbnail %d (%s) ...", i, videos[i]["thumbnail"])
                    
                    # build output thumbnail filename
                    thumbExtension = os.path.splitext(videos[i]["thumbnail"])[1]
                    thumbFilename  = videos[i]["date"].strftime("%m%d%H%M") + "_" + str(videos[i]["duration"]) + thumbExtension
                    
                    # try to download the thumbnail
                    thumbUrl = self._downloadThumbnail(videos[i]["thumbnail"], self.config["downloadDirectory"] + "/" + thumbFilename)

                    with self.mutex:
                        self.videos[i]["thumbnail"] = thumbUrl

                    logging.debug("thumbnail downloaded")

                logging.debug("All thumbnails are downloaded !")

            # clear the refresh event
            self.refreshEvent.clear()

            logging.debug("%s refreshed !", self.parser.id)

    #
    def _downloadThumbnail(self, p_url, p_outFilepath):
        thumbnailUrl = p_url
        
        try:
            # todo : 
            
            with open(p_outFilepath, 'wb') as outThumbFile:
                inThumbFile = urllib2.urlopen(p_url)
                outThumbFile.write(inThumbFile.read())
                
            thumbnailUrl = p_outFilepath

        except Exception as e:
            logging.error("Unable to download the file %s (%s)", p_url, str(e))
            thumbnailUrl = p_url
        
        return thumbnailUrl

    #
    def getVideos(self):
        self.mutex.acquire()
        videos = copy.deepcopy(self.videos)
        self.mutex.release()
        
        return videos

    #
    def getVideoInfo(self, p_videoId):
        
        with self.mutex:
            try:
                videoInfo = self.videos[p_videoId]
            except:
                logging.error("Invalid video id %d", p_videoId)
                videoInfo = None
        
        return videoInfo

    # force refreshing data
    def refresh(self):
        self.refreshEvent.set()

    # stop the thread
    def stop(self):
        self.isRunning = False
        self.refresh()  # force a refresh to go out of the main loop
