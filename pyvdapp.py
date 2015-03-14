#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#----------------------------------------------
# API definition for pyvd
#----------------------------------------------
#
# VIDEO CHANNELS:
#
# Request videos channels : /channels
# Request to refresh the video list of a channel : /<channel_id>/reload
# Request the videos list of a channel : /<channel_id>/videos
#
# VIDEOS:
#
# Request a video info  : /video/info/<video_id>
#
# DOWNLOAD :
#
# add a video in the download list : /video/add/<video_id>
# remove a video from the download list: /video/delete/<video_id>
# configure a video in the download list /video/configure/<video_id>
# start downloading : /download/start
# cancel downloading : /download/cancel
#
# TOOL CONFIGURATION :
#
from flask import Flask, make_response
from flask import send_from_directory
from flask import jsonify
from flask import render_template
from flask import url_for
from PIL import Image
import pyvd.manager
import os
import sys

#----------------------------------------------
# Flask initialization
#----------------------------------------------
app = Flask(__name__)

#----------------------------------------------
# manager initialization
#----------------------------------------------
pyvdManager = pyvd.manager.Manager("channels")

#----------------------------------------------
# entry point
#----------------------------------------------

#
# pyvd index (entry point) : /
#
@app.route("/")
def handle_index_request():
    channels = pyvdManager.getChannels()
    return render_template('index.html', channels=channels)

#----------------------------------------------
# JSON API
#----------------------------------------------

#
# Request videos channels : /api/1.0/channels
#
@app.route("/api/1.0/channels", methods=['GET'])
def handle_video_channels_request():
    channels = pyvdManager.getChannels()
    return make_response(jsonify({'channels': channels}), 200)

#
# Request video channel list reloading : /api/1.0/<channelId>/reload
#
@app.route("/api/1.0/<int:p_channelId>/reload", methods=['GET'])
def handle_reload_request(p_channelId):
    pyvdManager.refreshChannel(p_channelId)
    return make_response("OK", 200)

#
# Request video channel list : /api/1.0/<channelId>/videos
#
@app.route("/api/1.0/<int:p_channelId>/videos", methods=['GET'])
def handle_channel_videos_list_request(p_channelId):
    videos = pyvdManager.getVideos(p_channelId)
    return make_response(jsonify({'channel' : p_channelId, 'videos': videos}), 200)

#
# Request video info  : /api/1.0/video/info/<video_id>
#
@app.route("/api/1.0/video/info/<int:p_videoId>", methods=['GET'])
def handle_video_info_request(p_videoId):
    video = pyvdManager.getVideoInfo(p_videoId)
    return make_response(jsonify({'video': video}), 200)

#
# add a video in the download list : /api/1.0/video/add/<video_id>
#
@app.route("/api/1.0/video/add/<int:p_videoId>", methods=['POST'])
def handle_video_add_request(p_videoId):
    pyvdManager.addVideoToDownloadList(p_videoId)
    return make_response("OK", 200)

#
# remove a video from the download list: /api/1.0/video/delete/<video_id>
#
@app.route("/api/1.0/video/remove/<int:p_videoId>", methods=['GET'])
def handle_video_remove_request(p_videoId):
    pyvdManager.removeVideoFromDownloadList(p_videoId)
    return make_response("OK", 200)

#
# configure a video in the download list /api/1.0/video/configure/<video_id>
#
@app.route("/api/1.0/video/configure/<int:p_videoId>", methods=['POST'])
def handle_video_configure_request(p_videoId):
    #todo
    return make_response("OK", 200)


#----------------------------------------------
# Common routes handling
#----------------------------------------------

#
# Request favicon
#
@app.route('/favicon.ico')
def handle_favicon_request():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#
# Error handler
#
@app.errorhandler(404)
def handle_error(error):
    return "Error {}".format(error.code), error.code

#----------------------------------------------
# Main
#----------------------------------------------
if __name__ == "__main__":

    # load the configuration
    if not pyvdManager.loadConfig():
        print "ERROR !"
        #TODO
        sys.exit(-1)

    # start the API manager
    pyvdManager.start()

    # run the Flask application
    app.run(debug=True)

    # stop the API manager
    pyvdManager.stop()
