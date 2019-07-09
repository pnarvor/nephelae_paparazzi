import os

from ivy.std_api import *
import logging

from . import messages as pmsg
from . import PprzUavBase

class PprzInterface:

    """PprzInterface

    Main class to launch all uavs from. Will listen to gps messages and 
    spawn a new PprzUavBase (or derived type) if uavId of the GPS message
    if not already known.

    A new Uav instance is built through a factory pattern 'build_uav_callback'.
    This callback can be redefined to spawn other type of Uavs.
    """


    def __init__(self, ivyIpp="127.255.255.255:2010",
                 build_uav_callback=lambda uavId, navRef: PprzUavBase(uavId, navRef)):
        self.ivyIpp   = ivyIpp
        self.navFrame = None
        self.uavs     = {}
        self.ivyBinds = []
        self.running  = False
        self.build_uav_callback = build_uav_callback


    def start(self):

        IvyInit("PprzInterface_" + str(os.getpid()))
        logging.getLogger('Ivy').setLevel(logging.WARN)
        IvyStart("127.255.255.255:2010")
        
        # Finding a Navigation frame
        while self.navFrame is None:
            print("Waiting for NAVIGATION_REF message...")
            try:
                self.navFrame = pmsg.grab_one(pmsg.NavigationRef, timeout=2.0)
            except Exception as e:
                pass
        print(self.navFrame)
        self.ivyBinds.append(pmsg.Gps.bind(self.found_uav_callback))
        self.running = True


    def stop(self):
        if self.running:
            print("Shutdown... ", end="")
            for bindId in self.ivyBinds:
                IvyUnBindMsg(bindId)
            for uav in self.uavs.values():
                if uav is not None:
                    uav.terminate()
            uavs = {}
            IvyStop()
            self.running = False
            print("Complete.")


    def found_uav_callback(self, msg):
        uavId = msg.uavId
        if not uavId in self.uavs.keys():
            self.uavs[uavId] = self.build_uav_callback(uavId, self.navFrame)
            print("Found UAV, id :", uavId)


    def __getitem__(self, key):
        return self.uavs[key]



