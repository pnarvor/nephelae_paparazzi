from ivy.std_api import *
import logging

from . import messages as pmsg

class PprzUav:

    def __init__(self, uavId, navFrame,
                       gpsObservers=[],
                       sensorObservers=[]):

        self.id          = uavId
        self.navFrame    = navFrame
        self.gps         = []
        self.ptu         = []
        self.cloudSensor = []

        self.ivyBinds = []
        self.ivyBinds.append(pmsg.Gps.bind(self.gps_callback, self.id))
        self.ivyBinds.append(pmsg.Ptu.bind(self.ptu_callback, self.id))
        self.ivyBinds.append(pmsg.CloudSensor.bind(self.cloud_sensor_callback, self.id))

    def terminate(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)
                          
    def gps_callback(self, msg):
        self.gps.append(msg)

    def ptu_callback(self, msg):
        self.ptu.append({'gps': self.gps[-1], 'data': msg})

    def cloud_sensor_callback(self, msg):
        self.cloudSensor.append({'gps': self.gps[-1], 'data': msg})

