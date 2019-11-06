#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal
import time

from ivy.std_api import *
import logging

from nephelae_mesonh    import MesonhDataset
from nephelae_paparazzi import PprzSimulation, PprzMissionUav, print_status, PprzUavBase
from nephelae_paparazzi.missions import MissionFactory
from nephelae_paparazzi.missions.rules import *

# mesonhFiles = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc'
# mesonhFiles = '/home/pnarvor/work/nephelae/data/nephelae-remote/Nephelae_tmp/download/L12zo.1.BOMEX.OUT.*.nc'
mesonhFiles = '/home/pnarvor/work/nephelae/data/nephelae-remote/MesoNH02/bomex_hf.nc'
mesonhDataset = MesonhDataset(mesonhFiles)

class Logger:

    def __init__(self):
        pass

    def add_sample(self, msg):
        print(msg, end="\n\n", flush=True)

    def add_gps(self, msg):
        print(msg, end="\n\n", flush=True)

    def notify_status(self, status):
        print_status(status, flush=True)


laceFactory = MissionFactory("Lace", {
    'start_x'              : SimpleBounds([-10000.0, 10000.0], 'start_x'),
    'start_y'              : SimpleBounds([-10000.0, 10000.0], 'start_y'),
    'start_z'              : SimpleBounds([300.0, 4000.0], 'start_z'),
    'first_turn_direction' : AllowedValues([-1.0, 1.0], 'first_turn_direction'),
    'circle_radius'        : SimpleBounds([50.0, 500.0], 'circle_radius'),
    'drift_x'              : SimpleBounds([-10.0, 10.0], 'drift_x'),
    'drift_y'              : SimpleBounds([-10.0, 10.0], 'drift_y'),
    'drift_z'              : ParameterRules([DefaultValue(7.2, 'drift_z'),
                                             SimpleBounds([-10.0, 10.0], 'drift_z')],
                                             'drift_z'),

})


def build_uav(uavId, navRef):
    uav = PprzMissionUav(uavId, navRef, [laceFactory])

    # Uncomment this for console output
    # uav.add_gps_observer(Logger())
    # uav.add_status_observer(Logger())
    return uav

interface = PprzSimulation(mesonhFiles,
                           ['RCT', 'WT', ['UT','VT']],
                           build_uav_callback=build_uav,
                           windFeedback=True)
# ### wind feedback only
# interface = ppint.PprzSimulation(mesonhFiles, [], build_uav_callback=None)
interface.start()

def stop():
    if interface.running:
        print("Shutting down... ", end='')
        sys.stdout.flush()
        interface.stop()
        print("Complete.")
        exit()
signal.signal(signal.SIGINT, lambda sig,fr: stop())

