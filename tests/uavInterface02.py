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

    def notify(self, sample):
        print(sample, end="\n\n")

interface = ppint.PprzInterface()
interface.start()

signal.signal(signal.SIGINT, lambda sig,fr: interface.stop())

uavs = []
while interface.running:
    for uav in interface.uavs.keys():
        if uav not in uavs:
            interface.uavs[uav].sensorObservers.append(Logger())
            uavs.append(uav)
    time.sleep(0.5)

