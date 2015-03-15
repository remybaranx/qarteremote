# -*- coding: utf-8 -*-

import threading
import urllib2

class Downloader(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)

#	
class HTTPDownloader(threading.Thread):
	
	def __init__(self, p_url, p_outputDirname, p_outputFilename=""):
#		super.__init__(self)
		threading.Thread.__init__(self)
		self.url = p_url
		self.outDirname  = p_outputDirname 
		self.outFilename = p_outputFilename
		self.blocksize   = 8192
	
	def run(self):
		
		# open the video file
		try:
			inVideoFile = urllib2.urlopen(self.url)
		except:
			print "Unable to open the HTTP video file"
			return False

		# extract the HTTP video file size
		meta = inVideoFile.info()
		inVideoFileSize = int(meta.getheaders("Content-Length")[0])

		# build output filename
#		if self.outFilename == "":
#			self.outFilename = # basename

		# open the output file
		outVideoFile = open(self.outDirname + "/" + self.outFilename, 'wb')

		if outVideoFile is None:
			print "Unable to open {} output video file".format(self.outDirname + "/" + self.outFilename)
			return False

		# read the HTTP video file and write it in the output video file
		currentOutFileSize = 0
		
		try:
			while True:
				readBuffer = inVideoFile.read(self.blocksize)

				if not readBuffer:
					break

				outVideoFile.write(readBuffer)
				currentOutFileSize += len(readBuffer)
	
		except:
			print "Unable to read the HTTP video file {}".format(self.url)
			return False
	
		finally:
			outVideoFile.close()
	
		return True

#	
class RTMPDownloader(Downloader):
	pass
