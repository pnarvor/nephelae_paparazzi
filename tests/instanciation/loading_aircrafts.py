#! /usr/bin/python3

import sys
sys.path.append('../../')
import os
import signal
import time
import yaml

from nephelae_mesonh            import MesonhDataset
from nephelae_paparazzi         import Aircraft, AircraftLogger, PprzInterface, build_aircraft
from nephelae_paparazzi.plugins import MesonhProbe
from nephelae_paparazzi.utils   import send_lwc
from nephelae_paparazzi.common  import PprzMessage, messageInterface

from nephelae_paparazzi.plugins.loaders import load_plugins

config = None
with open('config_files/aircrafts.yaml','r') as f:
    config = yaml.safe_load(f)

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
    
    uav = build_aircraft(uavId, navRef, config['aircrafts'])

    uav.add_gps_observer(logger)
    uav.add_sensor_observer(logger)
    uav.add_status_observer(logger)

    uav.start()
    return uav

logger = AircraftLogger(quiet=True)
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

