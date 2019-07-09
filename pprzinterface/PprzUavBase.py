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
        self.notify_gps(msg)
        self.gps.append(msg)


    def add_gps_observer(self, observer):
        if not gps_notifiable(observer):
            raise AttributeError("Observer is not notifiable")
        self.gpsObservers.append(observer)


    def add_sensor_observer(self, observer):
        if not sensor_sample_notifiable(observer):
            raise AttributeError("Observer is not notifiable")
        self.sensorObservers.append(observer)


    def notify_gps(self, gps):
        for gpsObserver in self.gpsObservers:
            gpsObserver.add_gps(gps)


    def notify_sensor_sample(self, sample):
        for sensorObserver in self.sensorObservers:
            sensorObserver.add_sample(sample)
