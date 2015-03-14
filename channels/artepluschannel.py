# -*- coding: utf-8 -*-

import pyvd.channel
import json
import urllib2
import re

class ArtePlusChannel(pyvd.channel.Channel):
    
    BASE_URL = "http://www.arte.tv"
    ROOT_URL = BASE_URL + "/guide/fr/plus7.json"

    #
    def __init__(self):
        self.id = "arteplus"
        self.name = "Arte +7"
        self.jsonStreamsUrlRegex = re.compile("^.*arte_vp_url='(http.*PLUS7-F/ALL/ALL.json).*", re.MULTILINE)

    #
    def filterHTTPStreams(self, p_streams):
        streams = []

        # search all HTTP streams in the list of streams    
        for key in p_streams.keys():
            if "HTTP" in key:
                stream = {}

                # get stream language
                if "VA" in p_streams[key]["versionShortLibelle"]:
                    stream["language"] = "de"
                elif "VF" in p_streams[key]["versionShortLibelle"]:
                    stream["language"] = "fr"
                else:
                    # skip this stream
                    continue

                # get stream quality
                if "SD" in p_streams[key]["quality"]:
                    stream["quality"] = "Low"
                elif "HD" in p_streams[key]["quality"]:
                    stream["quality"] = "High"
                elif "MD" in p_streams[key]["quality"]:
                    stream["quality"] = "Medium"
                else:
                    # skip this stream
                    continue

                # get stream width x height
                stream["videosize"] = "{} x {}".format(p_streams[key]["width"], p_streams[key]["height"])
 
                # get stream url                                
                stream["url"] = p_streams[key]["url"]

                # add the new stream in the list
                streams.append(stream)

                # remove the entry in the streams dictionary
                del p_streams[key]
    
        return streams        

    #
    def filterRTMPStreams(self, p_streams):
        pass

    #
    def filterStreams(self, p_streams):
        streams = {}
        streams["HTTP"] = self.filterHTTPStreams(p_streams)
#        streams["RTMP"] = filterRTMPStreams(p_streams)
        return streams
        
    #
    def getPageContent(self, p_url):
        
        # get page content
        try:
            content = urllib2.urlopen(p_url).read()
        except IOError as e:
            print "urllib2 IO error"
            return None
            
        return content

    #
    def parseJSONStreamsFile(self, p_url):
    
#        print p_url

        # get JSON streams file
        jsonStreamsFile = self.getPageContent(p_url)
        
        if jsonStreamsFile is None:
            print "Unable to get the JSON stream file"
            return None

        # parse the JSON file
        streams = json.loads(jsonStreamsFile.decode('utf8', 'replace'))
    
        if streams == None:
            print "Unable to decode the JSON stream file"
            return None
            
        # extract all video streams from JSON data
        if not "videoJsonPlayer" in streams: 
            print "Unable to find the 'videoJsonPlayer' key in the JSON data"
            return None
            
        if not "VSR" in streams["videoJsonPlayer"]:
            print "Unable to find the 'VSR' key in the JSON data"
            return None
        
        return self.filterStreams(streams["videoJsonPlayer"]["VSR"])

    #
    def getVideoStreams(self, p_url):

        # get video page content
        pageContent = self.getPageContent(p_url)
        
        if pageContent == None:
            print "Unable to get video page content"
            return None
            
        # parse the video page content to extract the JSON file that contains all streams url
        regexResult = self.jsonStreamsUrlRegex.search(pageContent)

        if regexResult == None:
            print "Unable to find the JSON stream file URL"
            return None

        jsonStreamsUrl = regexResult.group(1)

        # parse the JSON streams file
        return self.parseJSONStreamsFile(jsonStreamsUrl)

    #
    def parse(self):
        
        # get the root page content
        rootContent = self.getPageContent(self.ROOT_URL)
        
        if rootContent == None:
            print "Unable to get the root page content"
            return False
            
        # parse the root page content
        rootContentDict = json.loads(rootContent.decode('utf8', 'replace'))

        if not "videos" in rootContentDict:
            print "Invalid rootContentDict"
            return False

        # loop on all the videos of the root page content
        videos = []
        for item in rootContentDict["videos"]:
            video = {}
            video["title"]      = item["title"]
            video["url"]        = self.BASE_URL + item["url"] + "?autoplay=1"
            video["thumbnail"]  = item["image_url"]
            video["date"]       = item["airdate_long"]
            video["duration"]  = item["duration"]
            video["pitch"]      = item["desc"]
            video["categories"] = item["video_channels"].split(", ")
            video["streams"]    = self.getVideoStreams(video["url"])
            
            videos.append(video)
        
        return videos

