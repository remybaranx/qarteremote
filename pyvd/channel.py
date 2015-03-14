# -*- coding: utf-8 -*-

import pyvd.pluginmount

class Channel(object):
    """
        A video channel.
    """
    __metaclass__ = pyvd.pluginmount.PluginMount

    def __init__(self):
        self.id   = ""      # A channel ID is a string without spaces, that identifies the channel ("arteplus" for example). 
        self.name = ""      # This is the full name of the channel. It could contain some spaces ("Arte Plus" for example)

    def parse(self):
        """
            Parse the raw videos list from the channel. 
            :return: a list of videos, where each video is a dictionary with the following keys :
                TODO
        """
        pass
