from ivy.std_api import *
import logging

from . import messages as pmsg

class PprzUav:

    def __init__(self, uavId, navFrame):

        self.id       = uavId
        self.navFrame = navFrame
        self.gps      = []

        self.binds = []
        self.binds.append(
            IvyBindMsg(lambda agent, msg: self.gps_callback(msg),
                       '(' + str(self.id) + ' GPS .*)'))

    def unbind(self):
        for bindId in self.binds:
            IvyUnBindMsg(bindId)
                          
    def gps_callback(self, msg):
        self.gps.append(pmsg.Gps(msg))


