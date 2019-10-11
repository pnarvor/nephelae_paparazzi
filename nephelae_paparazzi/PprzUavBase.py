from ivy.std_api import *
import logging
import random
import os
import time
import threading
from defusedxml.ElementTree import parse as xml_parse
import utm

from nephelae.types import MultiObserverSubject
from nephelae.types import SensorSample

from . import common
from .messages import Gps, FlightParam, NavStatus, ApStatus, Bat, MissionStatus, Config

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


def status_to_str(status):
    return 'UAV ' + status['id'] + ' status :'\
        + '\n  lat              : ' + str(status['lat'])\
        + '\n  long             : ' + str(status['long'])\
        + '\n  utm_east         : ' + str(status['utm_east'])\
        + '\n  utm_north        : ' + str(status['utm_north'])\
        + '\n  utm_zone         : ' + str(status['utm_zone'])\
        + '\n  alt              : ' + str(status['alt'])\
        + '\n  agl              : ' + str(status['agl'])\
        + '\n  roll             : ' + str(status['roll'])\
        + '\n  pitch            : ' + str(status['pitch'])\
        + '\n  heading          : ' + str(status['heading'])\
        + '\n  course           : ' + str(status['course'])\
        + '\n  speed            : ' + str(status['speed'])\
        + '\n  air_speed        : ' + str(status['air_speed'])\
        + '\n  climb            : ' + str(status['climb'])\
        + '\n  itow             : ' + str(status['itow'])\
        + '\n  flight_time      : ' + str(status['flight_time'])\
        + '\n  target_lat       : ' + str(status['target_lat'])\
        + '\n  target_long      : ' + str(status['target_long'])\
        + '\n  target_utm_east  : ' + str(status['target_utm_east'])\
        + '\n  target_utm_north : ' + str(status['target_utm_north'])\
        + '\n  target_alt       : ' + str(status['target_alt'])\
        + '\n  target_course    : ' + str(status['target_course'])\
        + '\n  target_climb     : ' + str(status['target_climb'])\
        + '\n  current_block_id : ' + str(status['current_block_id'])\
        + '\n  current_block    : ' + str(status['current_block'])\
        + '\n  block_time       : ' + str(status['block_time'])\
        + '\n  mission_time_left: ' + str(status['mission_time_left'])\
        + '\n  mission_task_list: ' + str(status['mission_task_list'])


def print_status(status, flush=True):
    print(status_to_str(status), flush=flush)


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
        super().__init__(['add_gps', 'add_sample', 'notify_status'])

        self.id          = uavId
        self.navFrame    = navFrame
        self.config      = None

        self.gpsObservers    = []
        self.sensorObservers = []

        self.blocks    = {}
        self.waypoints = {}

        self.config               = None
        self.status               = None
        self.currentGps           = None
        self.currentFlightParam   = None
        self.currentNavStatus     = None
        self.currentApStatus      = None
        self.currentBat           = None
        self.currentMissionStatus = None

        self.init_status()
        self.request_config()

        self.ivyBinds = []
        self.ivyBinds.append(Gps.bind(self.gps_callback, self.id))
        self.ivyBinds.append(FlightParam.bind(self.set_flight_param, self.id))
        self.ivyBinds.append(NavStatus.bind(self.set_nav_status, self.id))
        self.ivyBinds.append(ApStatus.bind(self.set_ap_status, self.id))
        self.ivyBinds.append(Bat.bind(self.set_bat, self.id))
        self.ivyBinds.append(MissionStatus.bind(self.set_mission_status, self.id))

        self.gps = [] # For convenience. To be removed
        print("Building uav")


    def init_status(self):
        self.status = {'id':self.id}
        self.status['lat']               = 'NA'
        self.status['long']              = 'NA'
        self.status['utm_east']          = 'NA'
        self.status['utm_north']         = 'NA'
        self.status['utm_zone']          = 'NA'
        self.status['alt']               = 'NA'
        self.status['agl']               = 'NA'
        self.status['roll']              = 'NA'
        self.status['pitch']             = 'NA'
        self.status['heading']           = 'NA'
        self.status['course']            = 'NA'
        self.status['speed']             = 'NA'
        self.status['air_speed']         = 'NA'
        self.status['climb']             = 'NA'
        self.status['itow']              = 'NA'
        self.status['flight_time']       = 'NA'
        self.status['target_lat']        = 'NA'
        self.status['target_long']       = 'NA'
        self.status['target_utm_east']   = 'NA'
        self.status['target_utm_north']  = 'NA'
        self.status['target_alt']        = 'NA'
        self.status['target_course']     = 'NA'
        self.status['target_climb']      = 'NA'
        self.status['current_block_id']  = 'NA'
        self.status['current_block']     = 'NA'
        self.status['block_time']        = 'NA'
        self.status['mission_time_left'] = 'NA'
        self.status['mission_task_list'] = 'NA'


    def terminate(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)


    def gps_callback(self, msg):
        self.currentGps = msg
        self.notify_gps(msg)
        self.gps.append(msg)


    def set_bat(self, msg):
        self.currentBat = msg
        # if not self.gps:
        #     return
        # sample = SensorSample('BAT', producer=self.id,
        #                       timeStamp=msg.stamp,
        #                       position=self.gps[-1] - self.navFrame,
        #                       data=[msg.throttle,
        #                             msg.voltage,
        #                             msg.amps, 
        #                             msg.flight_time,
        #                             msg.block_time,
        #                             msg.stage_time,
        #                             msg.energy])
        # self.notify_sensor_sample(sample)
       
        self.init_status

    def set_flight_param(self, flightParam):
        self.currentFlightParam = flightParam

        utmUav = utm.from_latlon(flightParam.lat, flightParam.long)
        self.status['lat']       = flightParam.lat
        self.status['long']      = flightParam.long
        self.status['utm_east']  = utmUav[0]
        self.status['utm_north'] = utmUav[1]
        self.status['utm_zone']  = str(utmUav[2]) + utmUav[3]
        self.status['alt']       = flightParam.alt
        self.status['agl']       = flightParam.agl
        self.status['roll']      = flightParam.roll
        self.status['pitch']     = flightParam.pitch
        self.status['heading']   = flightParam.heading
        self.status['course']    = flightParam.course
        self.status['speed']     = flightParam.speed
        self.status['air_speed'] = flightParam.airspeed
        self.status['climb']     = flightParam.climb
        self.status['itow']      = flightParam.itow


    def set_nav_status(self, navStatus):
        self.currentNavStatus = navStatus

        utmTarget = utm.from_latlon(navStatus.target_lat, navStatus.target_long)
        self.status['target_lat']       = navStatus.target_lat
        self.status['target_long']      = navStatus.target_long
        self.status['target_utm_east']  = utmTarget[0]
        self.status['target_utm_north'] = utmTarget[1]
        self.status['target_alt']       = navStatus.target_alt
        self.status['target_course']    = navStatus.target_course
        self.status['target_climb']     = navStatus.target_climb
        self.status['current_block_id'] = navStatus.cur_block
        self.status['current_block']    = self.blocks[navStatus.cur_block]
        self.status['block_time']       = navStatus.block_time


    def set_ap_status(self, apStatus):
        self.currentApStatus = apStatus
        self.status['flight_time'] = apStatus.flight_time
        self.notify_status(self.status)


    def set_mission_status(self, missionStatus):
        self.currentMissionStatus = missionStatus

        self.status['mission_time_left'] = missionStatus.remaining_time
        # self.status['mission_task_list'] = 'NA'


    # decide to keep these or not...
    def add_gps_observer(self, observer):
        self.attach_observer(observer, 'add_gps')


    def add_sensor_observer(self, observer):
        self.attach_observer(observer, 'add_sample')


    def add_status_observer(self, observer):
        self.attach_observer(observer, 'notify_status')


    def remove_gps_observer(self, observer):
        self.detach_observer(observer, 'add_gps')


    def remove_sensor_observer(self, observer):
        self.detach_observer(observer, 'add_sample')


    def remove_status_observer(self, observer):
        self.detach_observer(observer, 'notify_status')
    # decide to keep these or not... (up)

    def notify_gps(self, gps):
        self.add_gps(gps)


    def notify_sensor_sample(self, sample):
        self.add_sample(sample)

    
    def config_callback(self, config):
        if self.config is not None:
            return
        self.config = config
        IvyUnBindMsg(self.configBindId)
        # self.configThread.join() # this is blocking everything... why ?

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
        self.configBindId = Config.bind(self.config_callback,
                                        str(os.getpid()) + '_\d+',
                                        self.id)
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


    def flight_time(self):
        return self.currentApStatus.flight_time


    # def get_mission_list(self):





