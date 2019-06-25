import os

from ivy.std_api import *
import logging

from . import messages as pmsg
from .PprzUav import PprzUav

class PprzInterface:

    def __init__(self, ivyIpp="127.255.255.255:2010"):

        self.ivyIpp   = ivyIpp
        self.navFrame = None
        self.uavs     = {}
        self.ivyBinds = []
        self.running  = False

    def start(self):

        IvyInit("PprzInterface_" + str(os.getpid()))
        logging.getLogger('Ivy').setLevel(logging.WARN)
        IvyStart("127.255.255.255:2010")
        
        # Finding a Navigation frame
        while self.navFrame is None:
            print("Waiting for NAVIGATION_REF message...")
            try:
                self.navFrame = pmsg.grab_one(pmsg.NavigationRef,
                                              '(.* NAVIGATION_REF .*)',
                                              timeout=2.0)
            except Exception as e:
                pass
        print(self.navFrame)

        self.ivyBinds.append(
            IvyBindMsg(lambda agent, msg: self.find_uavs_callback(msg),
                       '(.* GPS .*)'))
        self.running = True

    def stop(self):
        if self.running:
            print("Shutdown... ", end="")
            for bindId in self.ivyBinds:
                IvyUnBindMsg(bindId)
            for uav in self.uavs.values():
                uav.terminate()
            uavs = {}
            IvyStop()
            self.running = False
            print("Complete.")

    def find_uavs_callback(self, msg):
        uavId = int(msg.split(' ')[0])
        if not uavId in self.uavs.keys():
            self.uavs[uavId] = PprzUav(uavId, self.navFrame)
            print("Found UAV, id :", uavId)

