#! /usr/bin/python3

import os
import sys
import argparse
import time
import threading

from ivy.std_api import *
import logging

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../')))
sys.path.append(PPRZ_HOME + "/var/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprzlink import messages_xml_map

ids = [200,201,202,203,204]
ivyInterface = IvyMessagesInterface()
time.sleep(0.5)

ac_id = 200
index = 1
msg = PprzMessage('datalink', 'MISSION_CUSTOM')
msg['ac_id']    = ac_id
msg['insert']   = 0
msg['index']    = 1
msg['type']     = 'LACE'
msg['duration'] = -1
msg['params']   = [1500.0,900.0,700.0, 0, 50.0, -7.0,-0.5,3.0]
ivyInterface.send(msg)

msg['type']     = 'RSTT'
msg['index']    = 2
msg['params']   = [-1500.0,900.0,700.0, 0, 50.0, -7.0,-0.5,3.0]
ivyInterface.send(msg)

msg['type']     = 'SPIR3'
msg['index']    = 3
msg['params']   = [0.0,2400.0,700.0, 900.0, 50.0, 200.0, -7.0,-0.5,3.0]
ivyInterface.send(msg)


def all_start_lace():
    for id in ids:
        append_lace(id)
        start_block(id, 6)

def all_start_rosette():
    for id in ids:
        append_rosette(id)
        start_block(id, 6)


def append_lace(ac_id, index=1):
    msg = PprzMessage('datalink', 'MISSION_CUSTOM')
    msg['ac_id']    = ac_id
    msg['insert']   = 0
    msg['index']    = index
    msg['type']     = 'LACE'
    msg['duration'] = -1
    # msg['params']   = [-10500.0,1500.0,1100.0, 0, 100.0, 0]
    # msg['params']   = [-1500.0,1500.0,2600.0, 0, 100.0, -7.5,-0.5,0]
    msg['params']   = [1500.0,900.0,700.0, 0, 50.0, -7.0,-0.5,0]
    # msg['params']   = [-1500.0,1500.0,2600.0, 0, 100.0, 0.0,0.0,0]
    ivyInterface.send(msg)


def append_rosette(ac_id, index=1):
    msg = PprzMessage('datalink', 'MISSION_CUSTOM')
    msg['ac_id']    = ac_id
    msg['insert']   = 0
    msg['index']    = index
    msg['type']     = 'RSTT'
    msg['duration'] = -1
    # msg['params']   = [-10500.0,1500.0,1100.0]
    msg['params']   = [1500.0,900.0,700.0, 0, 50.0, -7.0,-0.5,0]
    # msg['params']   = [-1500.0,1500.0,2600.0, 0, 100.0, -7.5,-0.5,0]
    ivyInterface.send(msg)


def next_mission(ac_id):
    msg = PprzMessage('datalink', 'NEXT_MISSION')
    msg['ac_id'] = ac_id
    ivyInterface.send(msg)


def goto_mission(ac_id, index):
    msg = PprzMessage('datalink', 'GOTO_MISSION')
    msg['ac_id'] = ac_id
    msg['mission_id'] = index
    ivyInterface.send(msg)


def end_mission(ac_id):
    msg = PprzMessage('datalink', 'END_MISSION')
    msg['ac_id'] = ac_id
    ivyInterface.send(msg)


def start_block(ac_id, index):
    msg = PprzMessage('ground', 'JUMP_TO_BLOCK')
    msg['block_id'] = index
    msg['ac_id'] = ac_id
    ivyInterface.send(msg)


lwc = 0
def lwc_value(ac_id, value):
    msg = PprzMessage('datalink', 'PAYLOAD_COMMAND')
    msg['ac_id']   = ac_id
    msg['command'] = [value]
    ivyInterface.send(msg)


def start_lace(ac_id):
    append_lace(ac_id)
    start_block(ac_id, 6)



