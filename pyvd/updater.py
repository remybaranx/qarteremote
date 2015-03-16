# -*- coding: utf-8 -*-

import threading
import copy
import pyvd.parser

class Updater(threading.Thread):
    
    def __init__(self, p_parser, p_config={}):
        threading.Thread.__init__(self)
        self.parser = p_parser
        self.config = p_config  # TODO make a default config if p_config is empty
        self.videos = []
        self.refreshEvent  = threading.Event()
        self.mutex         = threading.RLock()
        self.isRunning     = False
        
    def run(self):

        # sanity checks
        if self.parser is None:
            print "Invalid parser"
            return False

        # main update loop
        print "Start updater for {}".format(self.parser.id)
        self.isRunning = True
        
        while self.isRunning:

            # wait for a refresh event (or until the refresh period is elapsed)
            self.refreshEvent.wait(self.config["refreshPeriod"])

            if not self.isRunning:
                continue

            print "start refreshing {} ...".format(self.parser.id)

            videos = self.parser.parse()

            # update the videos list
            self.mutex.acquire()
            self.videos = videos
            self.mutex.release()

            # clear the refresh event
            self.refreshEvent.clear()

            print "{} refreshed !".format(self.parser.id)

    #
    def getVideos(self):
        self.mutex.acquire()
        videos = copy.deepcopy(self.videos)
        self.mutex.release()
        
        return videos

    #
    def getVideoInfo(self, p_videoId):
        
        self.mutex.acquire()

        try:
            videoInfo = self.videos[p_videoId]
        except:
            print "Invalid video id {}".format(p_videoId)
            videoInfo = None

        self.mutex.release()
        
        return videoInfo

    # force refreshing data
    def refresh(self):
        self.refreshEvent.set()

    # stop the thread
    def stop(self):
        self.isRunning = False
        self.refresh()  # force a refresh to go out of the main loop
