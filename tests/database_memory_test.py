#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal
import time

from nephelae.database          import NephelaeDataServer
from nephelae_mesonh            import MesonhDataset
from nephelae_paparazzi         import Aircraft, AircraftLogger, PprzInterface
from nephelae_paparazzi.plugins import MesonhProbe

# mesonhFiles = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc'
mesonhFiles = '/home/pnarvor/work/nephelae/data/nephelae-remote/MesoNH02/bomex_hf.nc'
mesonhDataset = MesonhDataset(mesonhFiles)


def build_uav(uavId, navRef):
    uav = Aircraft(uavId, navRef)
    uav.load_plugin(MesonhProbe, mesonhDataset,
                    ['RCT', 'WT', ['UT','VT'], 'THT', 'RRT', 'RVT'])

    # uav.add_gps_observer(logger)
    # uav.add_sensor_observer(logger)
    # uav.add_status_observer(logger)

    uav.add_gps_observer(database)
    uav.add_sensor_observer(database)

    uav.start()
    return uav

logger = AircraftLogger()

database = NephelaeDataServer()
database.enable_periodic_save(path='/home/pnarvor/work/nephelae/tmp/database_memory_tests.ndb', force=True)

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

