from ivy.std_api import *
import logging

from . import messages as pmsg

class PprzUav:

    def __init__(self, uavId, navFrame):

        self.id       = uavId
        self.navFrame = navFrame
        self.gps      = []
        self.ptu      = []

        self.ivyBinds = []
        self.ivyBinds.append(pmsg.Gps.bind(self.gps_callback, self.id))
        self.ivyBinds.append(pmsg.Ptu.bind(self.ptu_callback, self.id))

    def terminate(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)
                          
    def gps_callback(self, msg):
        self.gps.append(msg)

    def ptu_callback(self, msg):
        self.ptu.append(msg)

