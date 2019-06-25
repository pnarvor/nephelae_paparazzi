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

import nephelae_pprzinterface.messages as pmsg

IvyInit("PprzInterface_" + str(os.getpid()))
logging.getLogger('Ivy').setLevel(logging.WARN)
IvyStart("127.255.255.255:2010")

# msg = pmsg.grab_one(pmsg.Gps, timeout=2.0)
msg = pmsg.grab_one(pmsg.NavigationRef, timeout=10.0)
print(msg)

