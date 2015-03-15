#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("channels")

import artepluschannel
import pyvd.downloader

p = artepluschannel.ArtePlusChannel()
videos = p.parse() 

print videos[3]

d = pyvd.downloader.HTTPDownloader(videos[3]["streams"]["HTTP"]["fr"]["Low"]["url"], "/tmp", "toto.mp4")
d.start()
d.join()

#import urllib2


#print "downloading {}".format(videos[0]["streams"]["HTTP"]["fr"]["Low"]["url"])

#u = urllib2.urlopen(videos[0]["streams"]["HTTP"]["fr"]["Low"]["url"])
#file_name = "/tmp/essai.mp4" 
#f = open(file_name, 'wb')
#meta = u.info()
#file_size = int(meta.getheaders("Content-Length")[0])
#print "Downloading: %s Bytes: %s" % (file_name, file_size)

#file_size_dl = 0
#block_sz = 8192
#while True:
#    buffer = u.read(block_sz)
#    if not buffer:
#        break
#
#    file_size_dl += len(buffer)
#    f.write(buffer)
#    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
#    status = status + chr(8)*(len(status)+1)
#    print status,
#
#f.close()

#
#import re
#regex = re.compile("$.*arte_vp_url=\'(http.*PLUS7-F/ALL/ALL.json)", re.DOTALL)
#regex = re.compile("^.*arte_vp_url='(http.*PLUS7-F/ALL/ALL.json).*", re.MULTILINE)

#f = open("file.html", "r")
#data = f.read()

#g = regex.search(data)
#print g.group(1)

