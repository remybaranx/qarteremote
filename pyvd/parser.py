# -*- coding: utf-8 -*-

import pyvd.pluginmount

class Parser(object):
    """
        A video parser.
    """
    __metaclass__ = pyvd.pluginmount.PluginMount

    def __init__(self):
        self.id   = ""      # A channel ID is a string without spaces, that identifies the parsed channel ("arteplus" for example). 
        self.name = ""      # This is the full name of the parsed channel. It could contain some spaces ("Arte Plus" for example)

    def parse(self):
        """
            Parse the raw videos list from a channel. 
            :return: a list of videos, where each video is a dictionary with the following keys :
                TODO
        """
        pass
