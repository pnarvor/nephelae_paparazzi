#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal
import time

from ivy.std_api import *
import logging

from nephelae_paparazzi import PprzInterface, PprzUav

class Logger:

    def __init__(self):
        pass

    def add_sample(self, sample):
        print(sample, end="\n\n")

    def add_gps(self, gps):
        print(gps, end="\n\n")

def build_uav(uavId, navRef):
    uav = PprzUav(uavId, navRef)
    uav.add_sensor_observer(Logger())
    uav.add_gps_observer(Logger())
    return uav

interface = PprzInterface(build_uav_callback=build_uav)
interface.start()

signal.signal(signal.SIGINT, lambda sig,fr: interface.stop())

