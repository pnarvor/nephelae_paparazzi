import copy
import utm
import time

from nephelae.types  import SensorSample, Position
from ..common import messageInterface, PprzMessage


class MeteoStick:

    """
    MeteoStick
    
    Plugin to fetch data from the PTU sensor on the Skywalker-X6 of CNRM.
    """

    def __pluginmethods__():
        return [{'name'         : 'meteo_stick_callback',
                 'method'       : MeteoStick.meteo_stick_callback,
                 'conflictMode' : 'append'},
                {'name'         : 'add_sensor_observer',
                 'method'       : MeteoStick.add_sensor_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'remove_sensor_observer',
                 'method'       : MeteoStick.remove_sensor_observer,
                 'conflictMode' : 'abort'}
               ]


    def __initplugin__(self):
        self.add_notification_method('add_sample')
        self.ivyBinds.append(messageInterface.bind(self.meteo_stick_callback,
                             '(' + str(self.id) + ' METEO_STICK .*)'))


    def add_sensor_observer(self, observer):
        self.attach_observer(observer, 'add_sample')


    def remove_sensor_observer(self, observer):
        self.detach_observer(observer, 'add_sample')
    

    def meteo_stick_callback(self, msg):

        utmPos   = utm.from_latlon(msg['lat'], msg['lon'])
        position = Position(time.time(), 
                            utmPos[0] - self.navFrame.utm_east,
                            utmPos[1] - self.navFrame.utm_north,
                            msg['hmsl'] - self.navFrame.ground_alt)

        pressure = SensorSample('pressure', self.id, position.time(),
                                copy.deepcopy(position), [msg['pressure']])
        temperature = SensorSample('temperature', self.id, position.time(),
                                   copy.deepcopy(position), [msg['temperature']])
        humidity = SensorSample('humidity', self.id, position.time(),
                                copy.deepcopy(position), [msg['humidity']])
        airspeed = SensorSample('airspeed', self.id, position.time(),
                                copy.deepcopy(position), [msg['airspeed']])
        self.add_sample(pressure)
        self.add_sample(temperature)
        self.add_sample(humidity)
        self.add_sample(airspeed)


def build_meteo_stick(aircraft):
    aircraft.load_plugin(MeteoStick)
