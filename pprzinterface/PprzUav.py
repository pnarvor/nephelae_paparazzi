from ivy.std_api import *
import logging

from nephelae_base.types import SensorSample

from . import messages as pmsg
from . import MessageSynchronizer

class PprzUav:

    def __init__(self, uavId, navFrame,
                       gpsObservers=[],
                       sensorObservers=[]):

        self.id          = uavId
        self.navFrame    = navFrame
        self.gps         = []
        self.ptu         = []
        self.cloudSensor = []

        self.gpsObservers    = gpsObservers
        self.sensorObservers = sensorObservers

        self.ivyBinds = []
        self.ivyBinds.append(pmsg.Gps.bind(self.gps_callback, self.id))
        self.ivyBinds.append(pmsg.Ptu.bind(self.ptu_callback, self.id))
        self.ivyBinds.append(pmsg.CloudSensor.bind(self.cloud_sensor_callback, self.id))

    def terminate(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)
                          
    def gps_callback(self, msg):
        self.gps.append(msg)
        for gpsObserver in self.gpsObservers:
            gpsObserver.notify(msg)


    def ptu_callback(self, msg):

        if len(self.gps) == 0:
            return
        gps = self.gps[-1] # Sync appends here. See if better way
        self.ptu.append({'gps': gps, 'data': msg})
        
        # Converting pprz message to SensorSample type
        pSample = SensorSample(variableName='pressure',
                               timeStamp=msg.stamp - self.navFrame.stamp,
                               position=gps - self.navFrame,
                               data=[msg.pressure])
        tSample = SensorSample(variableName='temperature',
                               timeStamp=msg.stamp - self.navFrame.stamp,
                               position=gps - self.navFrame,
                               data=[msg.temperature])
        uSample = SensorSample(variableName='humidity',
                               timeStamp=msg.stamp - self.navFrame.stamp,
                               position=gps - self.navFrame,
                               data=[msg.humidity])
        oSample = SensorSample(variableName='ptuUnknown',
                               timeStamp=msg.stamp - self.navFrame.stamp,
                               position=gps - self.navFrame,
                               data=[msg.humidity])

        for observer in self.sensorObservers:
            observer.notify(pSample)
            observer.notify(tSample)
            observer.notify(uSample)
            observer.notify(oSample)

    def cloud_sensor_callback(self, msg):

        if len(self.gps) == 0:
            return
        gps = self.gps[-1] # Sync appends here. See if better way
        self.cloudSensor.append({'gps': gps, 'data': msg})

        # Converting pprz message to SensorSample type
        sample = SensorSample(variableName='LWC',
                              timeStamp=msg.stamp - self.navFrame.stamp,
                              position=gps - self.navFrame,
                              data=[msg.var_0,msg.var_1,msg.var_2,msg.var_3])

        for observer in self.sensorObservers:
            observer.notify(sample)


