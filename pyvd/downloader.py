# -*- coding: utf-8 -*-

import threading
import urllib2
import subprocess
import logging

#	
class HTTPDownloader(threading.Thread):
	
	def __init__(self, p_url, p_outputDirname, p_outputFilename="", p_blocksize=8192):
		threading.Thread.__init__(self)
		self.url = p_url
		self.outDirname  = p_outputDirname 
		self.outFilename = p_outputFilename
		self.blocksize   = p_blocksize

		# build output filename
		if self.outFilename == "":
			self.outFilename = self.url.split("/")[-1]
	
	def run(self):

        	logging.info("HTTP downloader started for %s to %s", self.url, self.outDirname + "/" + self.outFilename)

		# open the video file
		try:
			inVideoFile = urllib2.urlopen(self.url)
		except:
			logging.error("Unable to open the HTTP video file")
			return False

		# extract the HTTP video file size
		meta = inVideoFile.info()
		inVideoFileSize = int(meta.getheaders("Content-Length")[0])

        	logging.debug("metadata for the url : %s", str(meta))

		# open the output file
		outVideoFile = open(self.outDirname + "/" + self.outFilename, 'wb')

		if outVideoFile is None:
			logging.error("Unable to open %s output video file", self.outDirname + "/" + self.outFilename)
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

                	logging.debug("%d/%d read", currentOutFileSize, inVideoFileSize)
	
		except:
			logging.error("Unable to read the HTTP video file %s", self.url)
			return False
	
		finally:
			outVideoFile.close()
	
		return True

#	
class RTMPDownloader(threading.Thread):
	
    def __init__(self, p_host, p_url, p_outputDirname, p_outputFilename=""):
        threading.Thread.__init__(self)
        self.host = p_host
        self.url  = p_url
        self.outDirname  = p_outputDirname 
        self.outFilename = p_outputFilename
	
	# build output filename
	if self.outFilename == "":
		self.outFilename = self.url.split("/")[-1]
    
    def run(self):

        logging.info("RTMP downloader started for %s to %s", self.host + "/" + self.url, self.outDirname + "/" + self.outFilename)

        # build the rtmpdump command
        command = ["rtmpdump",  "-r",  self.host + "/" + self.url, "-o", self.outDirname + "/" + self.outFilename]

        # launch the command in a subprocess
        try:
            process = subprocess.Popen(command, stdout = subprocess.PIPE,  stderr = subprocess.STDOUT)
        except:
            logging.error("Unable to launch the command %s", " ".join(command))
            return False
        
        # monitor the subprocess (TODO)
        while True:
            line = process.stdout.readline()
            
            if not line:
                break;
        
        
	
		return True
