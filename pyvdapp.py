#! /usr/bin/python
# -*- coding: utf-8 -*-
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
import logging

#----------------------------------------------
# Flask initialization
#----------------------------------------------
app = Flask(__name__)
appName = os.path.splitext(os.path.basename(__file__))[0]

#----------------------------------------------
# manager initialization
#----------------------------------------------
pyvdManager = pyvd.manager.Manager("./conf")

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
@app.route("/api/1.0/<p_channelId>/reload", methods=['GET'])
def handle_reload_request(p_channelId):
    if pyvdManager.refreshChannel(p_channelId):
        return make_response("OK", 200)
        
    return make_response("ERROR", 400);

#
# Request video channel list : /api/1.0/<channelId>/videos
#
@app.route("/api/1.0/<p_channelId>/videos", methods=['GET'])
def handle_channel_videos_list_request(p_channelId):
    videos = pyvdManager.getVideos(p_channelId)

    if videos is None:
        return make_response("ERROR", 400);
    
    return make_response(jsonify({'channel' : p_channelId, 'videos': videos}), 200)

#
# Request video info  : /api/1.0/<p_channelId>/video/info/<video_id>
#
@app.route("/api/1.0/<p_channelId>/video/info/<int:p_videoId>", methods=['GET'])
def handle_video_info_request(p_channelId, p_videoId):
    videoInfo = pyvdManager.getVideoInfo(p_channelId, p_videoId)

    if videoInfo is None:
        return make_response("ERROR", 400);

    return make_response(jsonify({'video': videoInfo}), 200)

#
# get the current download list : /api/1.0/downloadlist
#
@app.route("/api/1.0/downloadlist", methods=['GET'])
def handle_download_list_request():
    downloadList = pyvdManager.getDownloadList()
    return make_response(jsonify({'downloadList': downloadList}), 200)

#
# add a video in the download list : /api/1.0/downloadlist/add/<p_channelId>/<video_id>
#
@app.route("/api/1.0/downloadlist/add/<p_channelId>/<int:p_videoId>", methods=['GET'])
def handle_video_add_request(p_channelId, p_videoId):
    if not pyvdManager.addToDownloadList(p_channelId, p_videoId):
        return make_response("ERROR", 400)

    return make_response("OK", 200)

#
# remove a video from the download list: /api/1.0/downloadlist/del/<p_channelId>/<video_id>
#
@app.route("/api/1.0/downloadlist/del/<p_channelId>/<video_id>", methods=['GET'])
def handle_video_remove_request(p_channelId, p_videoId):
    if not pyvdManager.delFromDownloadList(p_channelId, p_videoId):
        return make_response("ERROR", 400)

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

    # create logger
    logging.basicConfig(filename='./' + appName + '.log',
                        format='%(asctime)s::%(levelname)s::%(filename)s:%(lineno)d::%(message)s',
                        level=logging.DEBUG)
    logging.info("--------------- APPLICATION STARTED ----------------------")

    # load the configuration
    #TODO
    pyvdManager.loadSystemConfig()
    pyvdManager.loadUserConfig()
    
    # start the API manager
    pyvdManager.start()

    # run the Flask application
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        # stop the API manager
        pyvdManager.stop()
