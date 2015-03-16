# -*- coding: utf-8 -*-

import threading


class Updater(threading.Thread):
    
    def __init__(self):
        pass
        
    def run(self):
        pass







DEFAULT_THUMB_FOLDER = "REMOVE_static/thumbnails"
DEFAULT_USER_FOLDER  = "REMOVE_static/users"
DEFAULT_DATA_REFRESH_PERIOD = 15 * 60












class Updater(threading.Thread):

    # constructor
    def __init__(self, p_manager):
        threading.Thread.__init__(self)

        self.manager = p_manager
        self.isRunning = False
        self.refreshEvent  = threading.Event()
        self.refreshPeriod = DEFAULT_DATA_REFRESH_PERIOD

        self.userFolder = DEFAULT_USER_FOLDER
        self.thumbnailFolder = DEFAULT_THUMB_FOLDER

    # force refreshing data
    def refresh(self):
        self.refreshEvent.set()

    # stop the thread
    def stop(self):
        self.isRunning = False
        self.refresh()  # force a refresh to go out of the main loop

    # update all arte plus videos thumbnails
    def updateThumbnails(self, p_videos):
        for video in p_videos:
            video.thumbnailFilepath = getThumbnailPath( self.thumbnailFolder, video)

    # refresh Arte data
    def run(self):
        self.isRunning = True

        while self.isRunning:

            # wait for a refresh event
            self.refreshEvent.wait(self.refreshPeriod)

            if not self.isRunning:
                continue

            print "start refreshing..."

            # get the video list
            artePlusVideos = []
            artePlusParser = parsers.ArteTVParser(self.userFolder, 'fr', artePlusVideos)
            artePlusParser.parse()

            print "videos list received"

            if not self.isRunning:
                continue

            # get thumbnails
            self.updateThumbnails(artePlusVideos)

            print "videos thumbnails received"

            if not self.isRunning:
                continue

            print "videos infos received"

            # update videos in the manager
            self.manager.setArtePlusVideos(artePlusVideos)

            # clear the refresh event
            self.refreshEvent.clear()

            print "refreshed!"
