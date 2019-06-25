import os

from ivy.std_api import *
import logging

class PprzInterface:

    def __init__(self, ivyIpp="127.255.255.255:2010"):

        self.ivyIpp         = ivyIpp
        self.uavs           = {}
        self.referenceFrame = []
        self.initialized    = False
    
    def start(self):

        IvyInit("PprzInterface_" + str(os.getpid()))
        logging.getLogger('Ivy').setLevel(logging.WARN)
        IvyStart(self.ivyIpp)

        self.waitInitBind = IvyBindMsg(lambda agent, msg: self.wait_init(msg),
                                       '(.* NAVIGATION_REF .*)')

    def stop(self):
        
        for key in self.uavs.keys():
            self.uavs[key].stop()
        IvyStop()
        self.referenceFrame = []
        self.initialized    = False

    def wait_init(self, msg):

