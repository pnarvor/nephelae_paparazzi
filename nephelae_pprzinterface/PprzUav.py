from ivy.std_api import *
import logging

from . import messages as pmsg

class PprzUav:

    def __init__(self, uavId, navFrame):

        self.id       = uavId
        self.navFrame = navFrame
        self.gps      = []

        self.ivyBinds = []
        self.ivyBinds.append(pmsg.Gps.bind(self.gps_callback, self.id))

    def terminate(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)
                          
    def gps_callback(self, msg):
        self.gps.append(msg)


