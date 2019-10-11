#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal
import time

from ivy.std_api import *
import logging

from nephelae_mesonh    import MesonhDataset
from nephelae_paparazzi import PprzSimulation, PprzMesonhUav, print_status, PprzUavBase

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


def build_uav(uavId, navRef):
    # uav = PprzMesonhUav(uavId, navRef, mesonhFiles, ['RCT', 'WT', ['UT', 'VT']])
    # uav = PprzMesonhUav(uavId, navRef, MesonhDataset(mesonhFiles, ('time','VLEV','S_N_direction','W_E_direction')),

    # uav = PprzUavBase(uavId, navRef)
    uav = PprzMesonhUav(uavId, navRef, mesonhDataset, ['RCT', 'WT', ['UT', 'VT']])

    # Uncomment this for console output
    uav.add_sensor_observer(Logger())
    uav.add_gps_observer(Logger())
    uav.add_status_observer(Logger())
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

