from ivy.std_api import *
import logging

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


class PprzUavBase:


    def __init__(self, uavId, navFrame):

        self.id          = uavId
        self.navFrame    = navFrame

        self.gpsObservers    = []
        self.sensorObservers = []

        self.ivyBinds = []
        self.ivyBinds.append(pmsg.Gps.bind(self.gps_callback, self.id))

        self.gps = [] # For convenience. To be removed


    def terminate(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)


    def gps_callback(self, msg):
        for gpsObserver in self.gpsObservers:
            gpsObserver.add_gps(msg)

        self.gps.append(msg)


    def add_gps_observer(self, observer):
        if not gps_notifiable(observer):
            raise AttributeError("Observer is not notifiable")
        self.gpsObservers.append(observer)


    def add_sensor_observer(self, observer):
        if not sensor_sample_notifiable(observer):
            raise AttributeError("Observer is not notifiable")
        self.sensorObservers.append(observer)
