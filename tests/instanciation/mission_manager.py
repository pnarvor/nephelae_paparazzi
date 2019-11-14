#! /usr/bin/python3

import sys
sys.path.append('../../')
import os
import signal
import time

from nephelae_mesonh            import MesonhDataset
from nephelae_paparazzi         import Aircraft, AircraftLogger, PprzInterface
from nephelae_paparazzi.plugins import MesonhProbe
from nephelae_paparazzi.utils   import send_lwc
from nephelae_paparazzi.common  import PprzMessage, messageInterface

# from nephelae_paparazzi.missions       import MissionManager, MissionFactory
# from nephelae_paparazzi.missions.rules import *

from nephelae_paparazzi.missions.builders import build_mission_manager

factoriesDesc = {
    'Lace':{
        'parameters':{
            'start'                : [{'Length': [3]},
                                      {'SimpleBounds':[[[-10000.0, -10000.0,  300.0], 
                                                        [ 10000.0,  10000.0, 4000.0]]]}],
            'first_turn_direction' : [{'AllowedValues': [[-1.0, 1.0]]}],
            'circle_radius'        : [{'SimpleBounds':[[50.0, 500.0]]}],
            'drift'                : [{'Length': [3]},
                                      {'SimpleBounds':[[[-10.0, -10.0, -5.0],
                                                        [ 10.0,  10.0,  5.0]]]}]
        }
    }
}

def create_mission():
    interface.uavs['200'].create_mission('Lace',
                                         duration=-1.0,
                                         start=[-1500.0, 900.0, 700.0],
                                         first_turn_direction=1.0,
                                         circle_radius=80.0,
                                         drift=[-7.5,-0.5,0.0])


def create_mission_fail():
    # must fail because start not in bounds
    interface.uavs['200'].create_mission('Lace',
                                         duration=-1.0,
                                         start=[-15000.0, 900.0, 700.0],
                                         first_turn_direction=1.0,
                                         circle_radius=80.0,
                                         drift=[-7.5,-0.5,0.0])


def build_uav(uavId, navRef):
    uav = Aircraft(uavId, navRef)
    build_mission_manager(uav, **factoriesDesc)
    # uav.load_plugin(MissionManager, factories={'Lace':laceFactory})

    # uav.add_gps_observer(logger)
    # uav.add_sensor_observer(logger)
    # uav.add_status_observer(logger)

    uav.start()
    return uav

logger = AircraftLogger()
interface = PprzInterface(build_uav_callback=build_uav)

interface.start()

def stop():
    if interface.running:
        print("Shutting down... ", end='')
        sys.stdout.flush()
        interface.stop()
        print("Complete.")
        exit()
signal.signal(signal.SIGINT, lambda sig,fr: stop())

