import copy
import utm
import time

from nephelae.types  import SensorSample, Position
from ..common import messageInterface, PprzMessage


class Energy:

    """
    Energy
    
    Plugin to fetch data from the PTU sensor on the Skywalker-X6 of CNRM.
    """

    def __pluginmethods__():
        return [{'name'         : 'energy_callback',
                 'method'       : Energy.energy_callback,
                 'conflictMode' : 'append'},
                {'name'         : 'add_sensor_observer',
                 'method'       : Energy.add_sensor_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'remove_sensor_observer',
                 'method'       : Energy.remove_sensor_observer,
                 'conflictMode' : 'abort'}
               ]


    def __initplugin__(self):
        self.add_notification_method('add_sample')
        self.ivyBinds.append(messageInterface.bind(self.energy_callback,
                             '(' + str(self.id) + ' ENERGY .*)'))


    def add_sensor_observer(self, observer):
        self.attach_observer(observer, 'add_sample')


    def remove_sensor_observer(self, observer):
        self.detach_observer(observer, 'add_sample')
    

    def energy_callback(self, msg):
        
        position = copy.deepcopy(self.status.position)
        sample = SensorSample('energy',  self.id, position.t, 
            copy.deepcopy(position),
            [msg['throttle'], msg['voltage'], msg['current'],
             msg['power'],msg['charge'],msg['energy'],])
        self.add_sample(sample)


def build_energy(aircraft):
    aircraft.load_plugin(Energy)
