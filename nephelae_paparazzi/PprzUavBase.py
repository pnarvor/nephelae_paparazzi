from ivy.std_api import *
import logging
import random
import os
import time
import threading
from defusedxml.ElementTree import parse as xml_parse

from nephelae.types import MultiObserverSubject
from nephelae.types import SensorSample

from . import common
from . import messages as pmsg

def gps_notifiable(obj):
    notifyMethod = getattr(obj, 'add_gps', None)
    if not callable(notifyMethod):
        return False
    else:
        return True


def sensor_sample_notifiable(obj):
    notifyMethod = getattr(obj, 'add_sample', None)
    if not callable(notifyMethod):
        return False
    else:
        return True


class PprzUavBase(MultiObserverSubject):

    """PprzUavBase
    
    Base type for handling paparazzi uavs through the ivy-bus.
    This class is intended to be the base class for both simulated and real
    Uavs (but is not an abstract class / can be instanciated).
    Uavs are identified by their paparazzi id which are used to subscribe to
    GPS messages.

    This class implements a subscriber pattern for external classes to get
    both GPS and sensor information. (The subscribers must implement a
    'add_gps' method and a 'add_sample' respectively).

    """


    def __init__(self, uavId, navFrame):
        super().__init__(['add_gps', 'add_sample', 'add_flight_param'])

        self.id          = uavId
        self.navFrame    = navFrame
        self.config      = None

        self.gpsObservers    = []
        self.sensorObservers = []

        self.ivyBinds = []
        self.ivyBinds.append(pmsg.Gps.bind(self.gps_callback, self.id))
        self.ivyBinds.append(pmsg.Bat.bind(self.bat_callback, self.id))
        self.ivyBinds.append(pmsg.FlightParam.bind(self.flight_param_callback, self.id))
        self.ivyBinds.append(pmsg.NavStatus.bind(self.nav_status_callback, self.id))

        self.config    = self.request_config()
        self.blocks    = {}
        self.waypoints = {}

        self.currentFlightParam = None
        self.currentNavStatus   = None

        self.gps = [] # For convenience. To be removed
        print("Building uav")


    def terminate(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)


    def gps_callback(self, msg):
        self.notify_gps(msg)
        self.gps.append(msg)


    def bat_callback(self, msg):
        if not self.gps:
            return
        sample = SensorSample('BAT', producer=self.id,
                              timeStamp=msg.stamp,
                              position=self.gps[-1] - self.navFrame,
                              data=[msg.throttle,
                                    msg.voltage,
                                    msg.amps, 
                                    msg.flight_time,
                                    msg.block_time,
                                    msg.stage_time,
                                    msg.energy])
        self.notify_sensor_sample(sample)
       

    def flight_param_callback(self, flightParam):
        self.currentFlightParam = flightParam
        self.notify_flight_param(flightParam)


    def nav_status_callback(self, navStatus):
        self.currentNavStatus = navStatus


    def add_gps_observer(self, observer):
        self.attach_observer(observer, 'add_gps')


    def add_sensor_observer(self, observer):
        self.attach_observer(observer, 'add_sample')


    def add_flight_param_observer(self, observer):
        self.attach_observer(observer, 'add_flight_param')


    def notify_gps(self, gps):
        self.add_gps(gps)


    def notify_sensor_sample(self, sample):
        self.add_sample(sample)

    
    def notify_flight_param(self, flightParam):
        self.add_flight_param(flightParam) 

    
    def config_callback(self, config):
        if self.config is not None:
            return
        self.config = config
        IvyUnBindMsg(self.configBindId)
        self.configThread.join()

        self.parse_config()
        print("Got config :", self. config)
        

    def request_config(self):
        def config_request_loop(uavObj):
            count = 1
            while uavObj.config is None:
                IvySendMsg('ground ' + str(os.getpid()) + '_' + str(count) +
                           ' CONFIG_REQ ' + str(self.id))
                count = count + 1
                time.sleep(1.0)
        self.configBindId = pmsg.Config.bind(self.config_callback,
                                             str(os.getpid()) + '_\d+')
        self.configThread = threading.Thread(target=config_request_loop,
                                             args=(self,))
        self.configThread.start()


    def parse_config(self):
        with open(self.config.flight_plan.split('file://')[1], "r") as fplanFile:
            xmlBlocks = xml_parse(fplanFile).getroot()\
                        .find('flight_plan').find('blocks').getchildren()
            for b in xmlBlocks:
                self.blocks[int(b.get('no'))] = b.get('name')


    def current_block(self):
        return self.blocks[self.currentNavStatus.cur_block]
