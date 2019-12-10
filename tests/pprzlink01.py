#! /usr/bin/python3

import os
import sys
import argparse
import time
import signal

from ivy.std_api import *
import logging

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../')))
sys.path.append(PPRZ_HOME + "/var/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprzlink import messages_xml_map

try:
    msgs = messages_xml_map.get_msgs('test')
except Exception as e:
    print(e)
dico = messages_xml_map.message_dictionary
for msg_type in dico.keys():
    for msg in dico[msg_type]:
        print(msg_type, ":", msg)

ac_id = 24
ivyInterface = IvyMessagesInterface()
time.sleep(0.5)

world = None
uavid = None
def callback01(ac_id, msg, request_id):
    print(request_id, msg)
def callback02(ac_id, msg):
    print(msg)
ivyInterface.subscribe(callback01, '(.* WORLD_ENV_REQ .*)')
ivyInterface.subscribe(callback02, '(.* GPS .*)')
signal.signal(signal.SIGINT, lambda frame, sig: ivyInterface.stop())


