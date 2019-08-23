#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal

from ivy.std_api import *
import logging

def signal_handler(sig, frame):
    IvyStop()
    exit()
signal.signal(signal.SIGINT, signal_handler)
IvyInit("PprzInterface_" + str(os.getpid()))
logging.getLogger('Ivy').setLevel(logging.WARN)
IvyStart("127.255.255.255:2010")

from nephelae_paparazzi import PprzUav
from nephelae_paparazzi.messages import NavigationRef, grab_one

msg = grab_one(NavigationRef, timeout=10.0)

uav100 = PprzUav(str(100), msg)
uav101 = PprzUav(str(101), msg)

