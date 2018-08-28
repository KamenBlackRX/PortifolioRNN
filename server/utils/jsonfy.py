import json

class Jsonfy(object):
    def __init__(self, *args, **kargs):
        """ 
            Constructor for jsonfy
        """
        if __debug__:
            print ("Debug: Initalizing...")
        self.file=kargs['file']
        self.mode = kargs['mode']