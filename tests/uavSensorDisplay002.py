#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal
import time
import threading
import matplotlib.pyplot as plt
from   matplotlib import animation
import numpy as np

from ivy.std_api import *
import logging

from nephelae_mesonh    import MesonhDataset
from nephelae_paparazzi import PprzSimulation, PprzMesonhUav, print_status, PprzUavBase
from nephelae_paparazzi.utils import DataRtDisplay

mesonhFiles = '/home/pnarvor/work/nephelae/data/nephelae-remote/MesoNH02/bomex_hf.nc'
mesonhDataset = MesonhDataset(mesonhFiles)


dataType = 'RCT'
# dataType = 'WT'
dataDisplay = DataRtDisplay(dataType)
# dataDisplay.draw()
def build_uav(uavId, navRef):
    uav = PprzMesonhUav(uavId, navRef, mesonhDataset, ['RCT', 'WT', ['UT', 'VT']])
    uav.add_sensor_observer(dataDisplay)
    return uav

interface = PprzSimulation(mesonhFiles,
                           ['RCT', 'WT', ['UT','VT']],
                           build_uav_callback=build_uav,
                           windFeedback=False)
interface.start()

def stop():
    if interface.running:
        print("Shutting down... ", end='', flush=True)
        interface.stop()
        print("Complete.", flush=True)
        exit()
signal.signal(signal.SIGINT, lambda sig,fr: stop())


