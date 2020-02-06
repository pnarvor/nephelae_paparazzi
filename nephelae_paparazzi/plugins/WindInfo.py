import copy
import utm
import time

from nephelae.types  import SensorSample, Position
from ..common import messageInterface, PprzMessage


class WindInfo:

    """
    WindInfo
    
    Plugin to fetch data from the PTU sensor on the Skywalker-X6 of CNRM.
    """

    def __pluginmethods__():
        return [{'name'         : 'wind_info_callback',
                 'method'       : WindInfo.wind_info_callback,
                 'conflictMode' : 'append'},
                {'name'         : 'add_sensor_observer',
                 'method'       : WindInfo.add_sensor_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'remove_sensor_observer',
                 'method'       : WindInfo.remove_sensor_observer,
                 'conflictMode' : 'abort'}
               ]


    def __initplugin__(self):
        self.add_notification_method('add_sample')
        self.ivyBinds.append(messageInterface.bind(self.wind_info_callback,
                             '(ground_dl WIND_INFO ' + str(self.id) + ' .*)'))


    def add_sensor_observer(self, observer):
        self.attach_observer(observer, 'add_sample')


    def remove_sensor_observer(self, observer):
        self.detach_observer(observer, 'add_sample')
    

    def wind_info_callback(self, msg):
        
        position = copy.deepcopy(self.status.position)
        sample = SensorSample('wind_info',  self.id, position.t, 
            copy.deepcopy(position),
            [msg['east'], msg['north'], msg['up'], msg['airspeed']])
        self.add_sample(sample)


def build_wind_info(aircraft):
    aircraft.load_plugin(WindInfo)
