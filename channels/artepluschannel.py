# -*- coding: utf-8 -*-

import pyvd.channel
import json
import urllib2
import re

class ArtePlusChannel(pyvd.channel.Channel):
    
    BASE_URL = "http://www.arte.tv"
    ROOT_URL = BASE_URL + "/guide/fr/plus7.json"

    def __init__(self):
        self.id = "arteplus"
        self.name = "Arte +7"
		self.jsonStreamsUrlRegex = re.compile('(http.*PLUS7-F/ALL/ALL.json)', re.DOTALL)
    
    #
    def parse(self):
        
        # get the root page content
        rootContent = self.getPageContent(self.ROOT_URL)
        
        if rootContent == None:
            return False
            
        # parse the root page content
        rootContentDict = json.loads(rootContent.decode('utf8', 'replace'))

        if not rootContentDict.hasKey("videos"):
            print "Invalid rootContentDict"
            return False

        # loop on all the videos of the root page content
        videos = []
        for item in rootContentDict["videos"]:
            video = {}
            video["title"]	 	= item["title"]
            video["url"]		= self.BASE_URL + item["url"] + "?autoplay=1"
            video["thumbnail"]	= item["image_url"]
            video["date"]		= item["airdate_long"]
            video["duraction"]	= item["duration"]
            video["pitch"]		= item["desc"]
            video["categories"]	= item["video_channels"].split(", ")
			video["streams"]	= self.getVideoStreams(video["url"])

            videos.append(video)
        
        return videos

	#
	def getVideoStreams(self, p_url):

		# get video page content
		pageContent = self.getPageContent(p_url)
		
		if pageContent == None:
			return None
			
		# parse the video page content to extract the JSON file that contains all streams url
		jsonStreamsUrl = self.jsonStreamsUrlRegex.search(pageContent)

		if jsonStreamsUrl == None:
			return None

		# parse the JSON streams file
		return self.parseJSONStreamsFile(jsonStreamsUrl.group(0))

	#
	def parseJSONStreamsFile(self, p_url):
	
		# get JSON streams file
		jsonStreamsFile = self.getPageContent(p_url)
		
		if jsonStreamsFile is None:
			return None

		# parse the JSON file
        streams = json.loads(jsonStreamsFile.decode('utf8', 'replace'))

		if streams is None:
			return None

		# extract all video streams from JSON data
		if not streams.hasKey("videoJsonPlayer"):
			return None
			
		if not streams["videoJsonPlayer"].hasKey("VSR"):
			return None
		
		return self.filterStreams(streams["videoJsonPlayer"]["VSR"])

	#
	def filterStreams(self, p_streams):
		return p_streams
		

    #
    def getPageContent(self, p_url):
        
        # get page content
        try:
            content = urllib2.urlopen(p_url).read()
        except IOError as e:
            return None
            
        return content
