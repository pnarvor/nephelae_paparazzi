from ivy.std_api import *
import logging

from nephelae_base.types import SensorSample

from . import messages as pmsg
from .MessageSynchronizer import MessageSynchronizer

def notifiable(obj):
    notifyMethod = getattr(obj, 'add_sample', None)
    if not callable(notifyMethod):
        return False
    else:
        return True

class PprzUav:

    def __init__(self, uavId, navFrame):

        self.id          = uavId
        self.navFrame    = navFrame

        self.ptuSynchronizer         = MessageSynchronizer()
        self.cloudSensorSynchronizer = MessageSynchronizer()

        self.gpsObservers    = []
        self.sensorObservers = []

        self.ivyBinds = []
        self.ivyBinds.append(pmsg.Gps.bind(self.gps_callback, self.id))
        self.ivyBinds.append(pmsg.Ptu.bind(self.ptu_callback, self.id))
        self.ivyBinds.append(pmsg.CloudSensor.bind(self.cloud_sensor_callback, self.id))

        self.gps = [] # For convenience

    def terminate(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)
                          
    def gps_callback(self, msg):

        self.process_ptu_message_pair(
            self.ptuSynchronizer.update_left_channel(msg))
        self.process_cloud_sensor_message_pair(
            self.cloudSensorSynchronizer.update_left_channel(msg))

        for gpsObserver in self.gpsObservers:
            gpsObserver.add_sample(msg)

        self.gps.append(msg)

    def ptu_callback(self, msg):

        self.process_ptu_message_pair(
            self.ptuSynchronizer.update_right_channel(msg))

    def cloud_sensor_callback(self, msg):

        self.process_cloud_sensor_message_pair(
            self.cloudSensorSynchronizer.update_right_channel(msg))
    
    def process_ptu_message_pair(self, pair):

        if pair is None:
            return

        gps = pair[0]
        ptu = pair[1]
        # Converting pprz message to SensorSample type
        pSample = SensorSample(variableName='pressure', producer=self.id,
                               timeStamp=ptu.stamp - self.navFrame.stamp,
                               position=gps - self.navFrame,
                               data=[ptu.pressure])
        tSample = SensorSample(variableName='temperature', producer=self.id,
                               timeStamp=ptu.stamp - self.navFrame.stamp,
                               position=gps - self.navFrame,
                               data=[ptu.temperature])
        uSample = SensorSample(variableName='humidity', producer=self.id,
                               timeStamp=ptu.stamp - self.navFrame.stamp,
                               position=gps - self.navFrame,
                               data=[ptu.humidity])
        oSample = SensorSample(variableName='ptuUnknown', producer=self.id,
                               timeStamp=ptu.stamp - self.navFrame.stamp,
                               position=gps - self.navFrame,
                               data=[ptu.humidity])

        for observer in self.sensorObservers:
            observer.add_sample(pSample)
            observer.add_sample(tSample)
            observer.add_sample(uSample)
            observer.add_sample(oSample)

    def process_cloud_sensor_message_pair(self, pair):
        
        if pair is None:
            return

        gps   = pair[0]
        cloud = pair[1]
        # Converting pprz message to SensorSample type
        sample = SensorSample(variableName='LWC', producer=self.id,
                              timeStamp=cloud.stamp - self.navFrame.stamp,
                              position=gps - self.navFrame,
                              data=[cloud.var_0,cloud.var_1,cloud.var_2,cloud.var_3])

        for observer in self.sensorObservers:
            observer.add_sample(sample)

    def add_gps_observer(self, observer):
        if not notifiable(observer):
            raise AttributeError("Observer is not notifiable")
        self.gpsObservers.append(observer)

    def add_sensor_observer(self, observer):
        if not notifiable(observer):
            raise AttributeError("Observer is not notifiable")
        self.sensorObservers.append(observer)
