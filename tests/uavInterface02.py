#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal
import time

from ivy.std_api import *
import logging

import pprzinterface as ppint

class Logger:

    def __init__(self):
        pass

    def add_sample(self, sample):
        print(sample, end="\n\n")

    def add_gps(self, gps):
        print(gps, end="\n\n")

interface = ppint.PprzInterface()
interface.start()

signal.signal(signal.SIGINT, lambda sig,fr: interface.stop())

uavs = []
while interface.running:
    for uav in interface.uavs.keys():
        if uav not in uavs:
            interface.uavs[uav].add_sensor_observer(Logger())
            interface.uavs[uav].add_gps_observer(Logger())
            uavs.append(uav)
    time.sleep(0.5)

