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

def callback00(msg):
    msg = pmsg.UavMessage(msg)
    print(msg)

def callback01(msg):
    msg = pmsg.Gps(msg)
    print(msg)

def callback02(msg):
    msg = pmsg.NavigationRef(msg)
    print(msg)

IvyBindMsg(lambda agent, msg: callback00(msg), '(.* GPS .*)')
IvyBindMsg(lambda agent, msg: callback01(msg), '(.* GPS .*)')
IvyBindMsg(lambda agent, msg: callback02(msg), '(.* NAVIGATION_REF .*)')

