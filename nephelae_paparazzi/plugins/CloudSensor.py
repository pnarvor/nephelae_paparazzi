import copy
import utm
import time

from nephelae.types  import SensorSample, Position
from ..common import messageInterface, PprzMessage


class CloudSensor:

    """
    CloudSensor
    
    Plugin to fetch data from the Cloud sensor on the Skywalker-X6 of CNRM.
    """

    def __pluginmethods__():
        return [{'name'         : 'cloud_sensor_callback',
                 'method'       : CloudSensor.cloud_sensor_callback,
                 'conflictMode' : 'append'},
                {'name'         : 'add_sensor_observer',
                 'method'       : CloudSensor.add_sensor_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'remove_sensor_observer',
                 'method'       : CloudSensor.remove_sensor_observer,
                 'conflictMode' : 'abort'}
               ]


    def __initplugin__(self):
        self.add_notification_method('add_sample')
        self.ivyBinds.append(messageInterface.bind(self.cloud_sensor_callback,
                             '(' + str(self.id) + ' CLOUD_SENSOR .*)'))

    
    def add_sensor_observer(self, observer):
        self.attach_observer(observer, 'add_sample')


    def remove_sensor_observer(self, observer):
        self.detach_observer(observer, 'add_sample')
    

    def cloud_sensor_callback(self, msg):

        utmPos   = utm.from_latlon(msg['lat'], msg['lon'])
        position = Position(time.time(), 
                            utmPos[0] - self.navFrame.utm_east,
                            utmPos[1] - self.navFrame.utm_north,
                            msg['hmsl'] - self.navFrame.ground_alt)

        for index, value in enumerate(msg['raw']):
            self.add_sample(SensorSample('cloud_channel_'+str(index),
                                         self.id, position.time(),
                                         copy.deepcopy(position),
                                         [value]))


def build_cloud_sensor(aircraft):
    aircraft.load_plugin(CloudSensor)
