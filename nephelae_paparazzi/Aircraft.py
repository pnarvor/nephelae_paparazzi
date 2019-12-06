import os
import threading
import utm
import time

from nephelae.types import MultiObserverSubject, Pluginable, Position

from .common           import IvySendMsg, IvyUnBindMsg
from .messages         import Gps, FlightParam, NavStatus, ApStatus, Bat, MissionStatus, Config
from .plugins.loaders  import load_plugins


class AircraftStatus:
    
    """
    AircraftStatus

    Hold general information about an Aircraft.

    Is basically the concatenation of the paparazzi messages
    FLIGHT_PARAM, NAV_STATUS, AP_STATUS, BAT, MISSION_STATUS
    """

    def __init__(self, aircraftId, navFrame):
        
        self.aircraftId        = aircraftId
        self.navFrame          = navFrame
        self.position          = Position()

        self.lat               = 'NA'
        self.long              = 'NA'
        self.utm_east          = 'NA'
        self.utm_north         = 'NA'
        self.utm_zone          = 'NA'
        self.alt               = 'NA'
        self.agl               = 'NA'
        self.roll              = 'NA'
        self.pitch             = 'NA'
        self.heading           = 'NA'
        self.course            = 'NA'
        self.speed             = 'NA'
        self.air_speed         = 'NA'
        self.climb             = 'NA'
        self.itow              = 'NA'
        self.flight_time       = 'NA'
        self.target_lat        = 'NA'
        self.target_long       = 'NA'
        self.target_utm_east   = 'NA'
        self.target_utm_north  = 'NA'
        self.target_alt        = 'NA'
        self.target_course     = 'NA'
        self.target_climb      = 'NA'
        self.current_block_id  = 'NA'
        self.current_block     = 'NA'
        self.block_time        = 'NA'
        self.mission_time_left = 'NA'
        self.mission_task_list = 'NA'


    def __str__(self):
        return 'Aircraft ' + self.aircraftId + ' status :'\
            + '\n  time             : ' + str(self.position.t)\
            + '\n  lat              : ' + str(self.lat)\
            + '\n  long             : ' + str(self.long)\
            + '\n  utm_east         : ' + str(self.utm_east)\
            + '\n  utm_north        : ' + str(self.utm_north)\
            + '\n  utm_zone         : ' + str(self.utm_zone)\
            + '\n  alt              : ' + str(self.alt)\
            + '\n  agl              : ' + str(self.agl)\
            + '\n  roll             : ' + str(self.roll)\
            + '\n  pitch            : ' + str(self.pitch)\
            + '\n  heading          : ' + str(self.heading)\
            + '\n  course           : ' + str(self.course)\
            + '\n  speed            : ' + str(self.speed)\
            + '\n  air_speed        : ' + str(self.air_speed)\
            + '\n  climb            : ' + str(self.climb)\
            + '\n  itow             : ' + str(self.itow)\
            + '\n  flight_time      : ' + str(self.flight_time)\
            + '\n  target_lat       : ' + str(self.target_lat)\
            + '\n  target_long      : ' + str(self.target_long)\
            + '\n  target_utm_east  : ' + str(self.target_utm_east)\
            + '\n  target_utm_north : ' + str(self.target_utm_north)\
            + '\n  target_alt       : ' + str(self.target_alt)\
            + '\n  target_course    : ' + str(self.target_course)\
            + '\n  target_climb     : ' + str(self.target_climb)\
            + '\n  current_block_id : ' + str(self.current_block_id)\
            + '\n  current_block    : ' + str(self.current_block)\
            + '\n  block_time       : ' + str(self.block_time)\
            + '\n  mission_time_left: ' + str(self.mission_time_left)\
            + '\n  mission_task_list: ' + str(self.mission_task_list)


    def set_flight_param(self, flightParam):

        # Getting current mission time
        self.position.t = time.time() - self.navFrame.position.t
        utmUav = utm.from_latlon(flightParam.lat, flightParam.long)
        self.position.x = utmUav[0] - self.navFrame.position.x
        self.position.y = utmUav[1] - self.navFrame.position.y
        self.position.z = flightParam.alt

        self.currentFlightParam = flightParam

        self.lat       = flightParam.lat
        self.long      = flightParam.long
        self.utm_east  = utmUav[0]
        self.utm_north = utmUav[1]
        self.utm_zone  = str(utmUav[2]) + utmUav[3]
        self.alt       = flightParam.alt
        self.agl       = flightParam.agl
        self.roll      = flightParam.roll
        self.pitch     = flightParam.pitch
        self.heading   = flightParam.heading
        self.course    = flightParam.course
        self.speed     = flightParam.speed
        self.air_speed = flightParam.airspeed
        self.climb     = flightParam.climb
        self.itow      = flightParam.itow


    def set_nav_status(self, navStatus):
        self.currentNavStatus = navStatus

        utmTarget = utm.from_latlon(navStatus.target_lat, navStatus.target_long)
        self.target_lat       = navStatus.target_lat
        self.target_long      = navStatus.target_long
        self.target_utm_east  = utmTarget[0]
        self.target_utm_north = utmTarget[1]
        self.target_alt       = navStatus.target_alt
        self.target_course    = navStatus.target_course
        self.target_climb     = navStatus.target_climb
        self.current_block_id = navStatus.cur_block
        # To be replaced by the block name if parsing of config files in possible
        self.current_block    = str(navStatus.cur_block)
        self.block_time       = navStatus.block_time


    def set_ap_status(self, apStatus):
        self.currentApStatus = apStatus
        self.flight_time = apStatus.flight_time


    def set_mission_status(self, missionStatus):
        self.mission_time_left = missionStatus.remaining_time
        self.mission_task_list = missionStatus.index_list

    
    def to_dict(self):
        """
        Convert status in json compatible dictionary
        Consider creating a single dictionary to hold all attributes instead of
        separated attributes.
        """
        res = {}
        res['id']                = self.aircraftId
        res['lat']               = self.lat
        res['long']              = self.long
        res['utm_east']          = self.utm_east
        res['utm_north']         = self.utm_north
        res['utm_zone']          = self.utm_zone
        res['alt']               = self.alt
        res['agl']               = self.agl
        res['roll']              = self.roll
        res['pitch']             = self.pitch
        res['heading']           = self.heading
        res['course']            = self.course
        res['speed']             = self.speed
        res['air_speed']         = self.air_speed
        res['climb']             = self.climb
        res['itow']              = self.itow
        res['flight_time']       = self.flight_time
        res['target_lat']        = self.target_lat
        res['target_long']       = self.target_long
        res['target_utm_east']   = self.target_utm_east
        res['target_utm_north']  = self.target_utm_north
        res['target_alt']        = self.target_alt
        res['target_course']     = self.target_course
        res['target_climb']      = self.target_climb
        res['current_block_id']  = self.current_block_id
        res['current_block']     = self.current_block
        res['block_time']        = self.block_time
        res['mission_time_left'] = self.mission_time_left
        res['mission_task_list'] = self.mission_task_list
        
        return res




class Aircraft(MultiObserverSubject, Pluginable):

    """
    Aircraft
    
    Base class for handling paparazzi uavs through the ivy-bus. This class is
    intended to be extend with plugins.

    Base functionalities includes status and gps update, and config request.
    """

    def __init__(self, uavId, navFrame):
        MultiObserverSubject.__init__(self, ['add_gps', 'notify_status'])

        self.id          = uavId
        self.navFrame    = navFrame
        self.ivyBinds    = []

        self.config               = None
        self.status               = AircraftStatus(self.id, self.navFrame)
        self.currentGps           = None
        self.currentFlightParam   = None
        self.currentNavStatus     = None
        self.currentApStatus      = None
        self.currentBat           = None
        self.currentMissionStatus = None
        self.running              = False


    def start(self):
        self.running = True
        self.request_config()
        self.ivyBinds.append(Gps.bind(self.gps_callback, self.id))
        self.ivyBinds.append(FlightParam.bind(self.flight_param_callback, self.id))
        self.ivyBinds.append(NavStatus.bind(self.nav_status_callback, self.id))
        self.ivyBinds.append(ApStatus.bind(self.ap_status_callback, self.id))
        self.ivyBinds.append(Bat.bind(self.bat_callback, self.id))
        self.ivyBinds.append(MissionStatus.bind(self.mission_status_callback, self.id))


    def stop(self):
        for bindId in self.ivyBinds:
            IvyUnBindMsg(bindId)
        self.running = False


    def gps_callback(self, msg):
        self.currentGps = msg
        self.add_gps(msg)


    def bat_callback(self, msg):
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
      

    def flight_param_callback(self, flightParam):
        self.currentFlightParam = flightParam
        self.status.set_flight_param(flightParam)


    def nav_status_callback(self, navStatus):
        self.currentNavStatus = navStatus
        self.status.set_nav_status(navStatus)


    def ap_status_callback(self, apStatus):
        self.currentApStatus = apStatus
        self.status.set_ap_status(apStatus)

        # Notifying status observer only in ap_status callback because the 3
        # status message are sent in close sequence and this is the last one.
        self.notify_status(self.status)


    def mission_status_callback(self, missionStatus):
        self.currentMissionStatus = MissionStatus
        self.status.set_mission_status(missionStatus)


    def config_callback(self, config):
        if self.config is not None:
            return
        self.config = config
        IvyUnBindMsg(self.configBindId)
        # self.configThread.join() # this is blocking everything... why ?

        print("Got config :", self. config)
        
        # Ensure color is 12bit format #ffffff
        try:
            step = int((len(self.config.default_gui_color) - 1) / 3)
            self.config.default_gui_color = "#" +\
                self.config.default_gui_color[1:3] +\
                self.config.default_gui_color[1+step:step+3] +\
                self.config.default_gui_color[1+2*step:2*step+3]
        except Exception as e:
            warn("Could not retrieve color code :", e)
            self.config.default_gui_color = "#ffffff"


    def request_config(self):
        def config_request_loop(uavObj):
            count = 1
            while uavObj.config is None and self.running:
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


    def flight_time(self):
        return self.currentApStatus.flight_time


    # decide to keep these or not...
    def add_gps_observer(self, observer):
        self.attach_observer(observer, 'add_gps')


    def add_status_observer(self, observer):
        self.attach_observer(observer, 'notify_status')


    def remove_gps_observer(self, observer):
        self.detach_observer(observer, 'add_gps')


    def remove_status_observer(self, observer):
        self.detach_observer(observer, 'notify_status')
    # decide to keep these or not... (up)




