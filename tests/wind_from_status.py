#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal
import time

from nephelae_paparazzi import Aircraft, AircraftLogger, PprzInterface
from nephelae_paparazzi.plugins import WindFromStatus

def build_uav(uavId, navRef):
    uav = Aircraft(uavId, navRef)
    uav.load_plugin(WindFromStatus)

    # uav.add_gps_observer(logger)
    # uav.add_status_observer(logger)
    uav.attach_observer(logger, 'add_sample')

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

