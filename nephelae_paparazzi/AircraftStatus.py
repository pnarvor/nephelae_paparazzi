import time
import utm
from copy import deepcopy

from nephelae.types import Position

class AircraftStatus:
    
    """
    AircraftStatus

    Hold general information about an Aircraft.

    Is basically the concatenation of the paparazzi messages
    FLIGHT_PARAM, NAV_STATUS, AP_STATUS, BAT, MISSION_STATUS
    """

    def __init__(self, aircraftId, navFrame):
        
        self.aircraftId        = str(aircraftId)
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
            + '\n  local_t          : ' + str(self.position.t)\
            + '\n  local_x          : ' + str(self.position.x)\
            + '\n  local_y          : ' + str(self.position.y)\
            + '\n  local_z          : ' + str(self.position.z)\
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


    def one_line_str(self):
        output = "AircraftStatus_" + self.aircraftId  + ", " +\
                 str(self.position.t)  + ", " +\
                 str(self.position.x)  + ", " +\
                 str(self.position.y)  + ", " +\
                 str(self.position.z)  + ", " +\
                 str(self.lat)  + ", " +\
                 str(self.long)  + ", " +\
                 str(self.utm_east)  + ", " +\
                 str(self.utm_north)  + ", " +\
                 str(self.utm_zone)  + ", " +\
                 str(self.alt)  + ", " +\
                 str(self.agl)  + ", " +\
                 str(self.roll)  + ", " +\
                 str(self.pitch)  + ", " +\
                 str(self.heading)  + ", " +\
                 str(self.course)  + ", " +\
                 str(self.speed)  + ", " +\
                 str(self.air_speed)  + ", " +\
                 str(self.climb)  + ", " +\
                 str(self.itow)  + ", " +\
                 str(self.flight_time)  + ", " +\
                 str(self.target_lat)  + ", " +\
                 str(self.target_long)  + ", " +\
                 str(self.target_utm_east)  + ", " +\
                 str(self.target_utm_north)  + ", " +\
                 str(self.target_alt)  + ", " +\
                 str(self.target_course)  + ", " +\
                 str(self.target_climb)  + ", " +\
                 str(self.current_block_id)  + ", " +\
                 str(self.current_block)  + ", " +\
                 str(self.block_time)  + ", " +\
                 str(self.mission_time_left)  + ", " +\
                 str(self.mission_task_list)
        return output


    def set_flight_param(self, flightParam):

        # Getting current mission time
        # self.position.t = time.time() - self.navFrame.position.t

        self.lat       = flightParam['lat']
        self.long      = flightParam['long']
        self.alt       = flightParam['alt']
        self.agl       = flightParam['agl']
        self.roll      = flightParam['roll']
        self.pitch     = flightParam['pitch']
        self.heading   = flightParam['heading']
        self.course    = flightParam['course']
        self.speed     = flightParam['speed']
        self.air_speed = flightParam['airspeed']
        self.climb     = flightParam['climb']
        self.itow      = flightParam['itow']

        utmUav = utm.from_latlon(self.lat, self.long)
        self.utm_east  = utmUav[0]
        self.utm_north = utmUav[1]
        self.utm_zone  = str(utmUav[2]) + utmUav[3]
        

        self.position.t = flightParam.timestamp - self.navFrame.position.t
        self.position.x = self.utm_east  - self.navFrame.position.x
        self.position.y = self.utm_north - self.navFrame.position.y
        self.position.z = self.alt       - self.navFrame.position.z



    def set_nav_status(self, navStatus):

        self.target_lat       = navStatus['target_lat']
        self.target_long      = navStatus['target_long']
        self.target_alt       = navStatus['target_alt']
        self.target_course    = navStatus['target_course']
        self.target_climb     = navStatus['target_climb']
        self.current_block_id = navStatus['cur_block']
        # To be replaced by the block name if parsing of config files in possible
        self.current_block    = navStatus['cur_block']
        self.block_time       = navStatus['block_time']

        utmTarget = utm.from_latlon(self.target_lat, self.target_long)
        self.target_utm_east  = utmTarget[0]
        self.target_utm_north = utmTarget[1]


    def set_ap_status(self, apStatus):
        self.flight_time = apStatus['flight_time']


    def set_mission_status(self, missionStatus):
        self.mission_time_left = missionStatus['remaining_time']
        self.mission_task_list = missionStatus['index_list']

    
    def to_dict(self):
        """
        Convert status in json compatible dictionary
        Consider creating a single dictionary to hold all attributes instead of
        separated attributes.
        """
        res = {}
        res['id']                = self.aircraftId
        res['local_t']           = self.position.t
        res['local_x']           = self.position.x
        res['local_y']           = self.position.y
        res['local_z']           = self.position.z
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

    def copy(self):
        return deepcopy(self)




