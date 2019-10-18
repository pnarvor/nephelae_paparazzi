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


class DisplayData:
    def __init__(self, dataType='WT', maxData=60):
        self.data     = {}
        self.dataType = dataType
        self.maxData  = maxData
        self.lock     = threading.Lock()

    def add_sample(self,msg):
        if msg.variableName != self.dataType:
            return
        with self.lock:
            if msg.producer not in self.data.keys():
                self.data[msg.producer] = [[0.0, 0.0]]*self.maxData
            self.data[msg.producer].append([msg.timeStamp, msg.data[0]])
            self.data[msg.producer][0:1] = []
    
    def get(self):
        res = {}
        with self.lock: 
            for key in self.data.keys():
                res[key] = np.copy(self.data[key])
        return res


dataType = 'RCT'
# dataType = 'WT'
dataObs = DisplayData(dataType)
def build_uav(uavId, navRef):
    uav = PprzMesonhUav(uavId, navRef, mesonhDataset, ['RCT', 'WT', ['UT', 'VT']])

    uav.add_sensor_observer(dataObs)

    # Uncomment this for console output
    # uav.add_sensor_observer(Logger())
    # uav.add_gps_observer(Logger())
    # uav.add_status_observer(Logger())
    return uav

interface = PprzSimulation(mesonhFiles,
                           ['RCT', 'WT', ['UT','VT']],
                           build_uav_callback=build_uav,
                           windFeedback=False)
interface.start()


varDisp = {}
fig,axes = plt.subplots(1,1)

def init():
    pass

def update(i):
    global varDisp
    data = dataObs.get()
    axes.clear()
    axes.set_title(dataObs.dataType)
    for key in data.keys():
        axes.plot(data[key][:,0], data[key][:,1], '--*', label=key)
    axes.legend(loc="lower left")
    axes.set_xlabel("Time (s)")

anim = animation.FuncAnimation(
    fig,
    update,
    init_func=init,
    interval = 1)

plt.show(block=False)



def stop():
    if interface.running:
        print("Shutting down... ", end='', flush=True)
        interface.stop()
        print("Complete.", flush=True)
        exit()
signal.signal(signal.SIGINT, lambda sig,fr: stop())

