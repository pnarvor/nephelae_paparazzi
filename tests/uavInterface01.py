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

import nephelae_pprzinterface as ppint

uav100 = ppint.PprzUavInterface(str(100,), None)
uav101 = ppint.PprzUavInterface(str(101,), None)

