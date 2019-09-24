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

import nephelae_paparazzi.messages as pmsg

# IvyInit("PprzInterface_" + str(os.getpid()))
# logging.getLogger('Ivy').setLevel(logging.WARN)
# IvyStart("127.255.255.255:2010")

def callback01(msg):
    print(msg)

def callback02(msg):
    print(msg)
    response = pmsg.WorldEnv.build(msg, 0.0,0.0,0.0)
    print(response.ivy_string())
    response.send()


# pmsg.Gps.bind(callback01)
# pmsg.NavigationRef.bind(callback01)
# pmsg.WorldEnvReq.bind(callback02, 19555)
# pmsg.WorldEnvReq.bind(callback02)
# pmsg.WorldEnv.bind(callback01)
# pmsg.WindInfo.bind(callback01)
# pmsg.Bat.bind(callback01)
# pmsg.FlightParam.bind(callback01)
pmsg.NavStatus.bind(callback01)



