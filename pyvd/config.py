# -*- coding: utf-8 -*-

import json

class Config:
    
    #
    def __init__(self, p_filename, p_data={}):
        self.filename = p_filename
        self.data     = p_data
        
    #
    def load(self):
        
        # open the configuration file and decode it
        try:
            with open(self.filename) as configFile:
                self.data = json.load(configFile)
        except IOError:
            print "Unable to open the file {}".format(self.filename)
            return False
        except:
            print "Unable to decode the file {}".format(self.filename)
            return False

        return True
        
    #
    def save(self):
        
        # open the configuration file and encode it
        try:
            with open(self.filename, "w") as configFile:
                json.dump(self.data, configFile)
        except IOError:
            print "Unable to open the file {}".format(self.filename)
            return False
        except:
            print "Unable to encode the file {}".format(self.filename)
            return False

        return True

    def __str__(self):
        return str(self.data)

    #
    def __getitem__(self, p_index):
        currentItem = self.data
        currentItemName = "[]"

        tokens = p_index.split('.')
        
        for token in tokens:
            if type(currentItem) is not dict:
                raise TypeError("item {} is not a dictionary ".format(currentItemName))
                return None
                
            if not currentItem.has_key(token):
                raise KeyError("Invalid token {} for item {}".format(token, currentItemName))
                return None
                
            currentItem = currentItem[token]
            currentItemName = token
        
        return currentItem
        
    #
    def __setitem__(self, p_index, p_item):
        tokens = p_index.split('.')
        
        currentItem = self.data
        for i in range(0, len(tokens)-1):
            if type(currentItem) is not dict:
                currentItem = dict()
                
            if not currentItem.has_key(tokens[i]): 
                currentItem[tokens[i]]=dict()
        
            if type(currentItem[tokens[i]]) is not dict:
                currentItem[tokens[i]] = dict()
        
            currentItem = currentItem[tokens[i]]
        
        currentItem[tokens[-1]] = p_item
        
