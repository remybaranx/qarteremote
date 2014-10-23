# -*- coding: utf-8 -*-

import threading
import parsers
import os
import urllib2
import pickle

#----------------------------------------------
# Some constants
#----------------------------------------------

NO_PREVIEW_THUMBNAIL = "static/medias/noPreview.png"
DEFAULT_THUMB_FOLDER = "static/data/thumbnails"
DEFAULT_USER_FOLDER  = "static/data/users"
DEFAULT_DATA_REFRESH_PERIOD = 15 * 60

#----------------------------------------------
# Some utils
#----------------------------------------------
def fetchPicture(p_url, p_filepath):
    """Get the image file for the thumbnail.

    Args:
    url -- image file URL
    path -- path where the file must be saved
    """
    try:
        with open(p_filepath, 'wb') as objfile:
            f = urllib2.urlopen(p_url)
            objfile.write(f.read())
        return p_filepath

    except:
        return NO_PREVIEW_THUMBNAIL

def getThumbnailPath(p_thumbnailFolder, p_video):
    """Return thumbnail path. If thumbnail is not already into the previews
    folder, he's downloaded.

    Args:
    p_thumbnailFolder -- folder to store the thumbnails
    p_video -- instance of VideoItem

    Returns:
    path of thumbnail
    """
    # Thumbnails are named with date, i.e. '2013 05 16, 13h01.jpg'
    thumbnailFilepath = os.path.join(p_thumbnailFolder, p_video.date.strip() + ".jpg")

    if not os.path.isfile(thumbnailFilepath):
        if p_video.pix is not None:
            return fetchPicture(p_video.pix, thumbnailFilepath)

        else:
            return NO_PREVIEW_THUMBNAIL

    return thumbnailFilepath

#----------------------------------------------
# handle Arte data update
#----------------------------------------------
class ArteWebRemoteUpdater(threading.Thread):

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
    def updateArtePlusThumbnails(self, p_artePlusVideos):
        for video in p_artePlusVideos:
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
            self.updateArtePlusThumbnails(artePlusVideos)

            print "videos thumbnails received"

            if not self.isRunning:
                continue

            print "videos infos received"

            # update videos in the manager
            self.manager.setArtePlusVideos(artePlusVideos)

            # clear the refresh event
            self.refreshEvent.clear()

            print "refreshed!"

#----------------------------------------------
# handle Arte data and web requests
#----------------------------------------------
class ArteWebRemoteManager:

    # ctor
    def __init__(self):

        self.artePlusVideos = []
        self.mutex = threading.Lock()

        # create and start the thread that updates Arte data from the Arte website
        self.updater = ArteWebRemoteUpdater(self)
        self.updater.start()
        self.updater.refresh()

    # release all resources
    def releaseResources(self):
        self.updater.stop()

    # set a new arte+7 video list
    def setArtePlusVideos(self, p_artePlusVideos):
        self.mutex.acquire()
        self.artePlusVideos = p_artePlusVideos
        self.mutex.release()

    # get Arte+7 videos
    def getArtePlusVideos(self):
        self.mutex.acquire()

        videosDict = []

        for video in self.artePlusVideos:
            videosDict.append(video.toDict())

        self.mutex.release()

        return videosDict

    # get Arte+7 video info
    def getArtePlusVideoInfo(self, p_videoId):
        self.mutex.acquire()
        videoInfo = self.artePlusVideos[p_videoId]
        self.mutex.release()

        return videoInfo.toDict()


    # add a Arte+7 video in the download list
    def addArtePlusVideo(self, p_videoId):
        return []

    # remove a Arte+7 video from the download list
    def removeArtePlusVideo(self, p_videoId):
        return []

    # configure a Arte+7 video of the download list
    def configureArtePlusVideo(self, p_videoId):
        return []

    # refresh the video list and thumbnails
    def refresh(self):
        self.updater.refresh()
