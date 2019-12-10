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

ac_id = 24
ivyInterface = IvyMessagesInterface()
time.sleep(0.5)


def append_lace(index=1):
    msg = PprzMessage('datalink', 'MISSION_CUSTOM')
    msg['ac_id']    = ac_id
    msg['insert']   = 0
    msg['index']    = index
    msg['type']     = 'LACE'
    msg['duration'] = -1
    # msg['params']   = [-10500.0,1500.0,1100.0, 0, 100.0, 0]
    # msg['params']   = [-1500.0,1500.0,2600.0, 0, 100.0, -7.5,-0.5,0]
    msg['params']   = [1500.0,900.0,700.0, 0, 50.0, -7.5,-0.5,0]
    # msg['params']   = [-1500.0,1500.0,2600.0, 0, 100.0, 0.0,0.0,0]
    ivyInterface.send(msg)


def append_rosette(index=1):
    msg = PprzMessage('datalink', 'MISSION_CUSTOM')
    msg['ac_id']    = ac_id
    msg['insert']   = 0
    msg['index']    = index
    msg['type']     = 'RSTT'
    msg['duration'] = -1
    # msg['params']   = [-10500.0,1500.0,1100.0]
    msg['params']   = [1500.0,900.0,700.0, 0, 50.0, -7.5,-0.5,0]
    # msg['params']   = [-1500.0,1500.0,2600.0, 0, 100.0, -7.5,-0.5,0]
    ivyInterface.send(msg)


def next_mission():
    msg = PprzMessage('datalink', 'NEXT_MISSION')
    msg['ac_id'] = ac_id
    ivyInterface.send(msg)


def goto_mission(index):
    msg = PprzMessage('datalink', 'GOTO_MISSION')
    msg['ac_id'] = ac_id
    msg['mission_id'] = index
    ivyInterface.send(msg)


def end_mission():
    msg = PprzMessage('datalink', 'END_MISSION')
    msg['ac_id'] = ac_id
    ivyInterface.send(msg)


def start_block(index):
    msg = PprzMessage('ground', 'JUMP_TO_BLOCK')
    msg['block_id'] = index
    msg['ac_id'] = ac_id
    ivyInterface.send(msg)


lwc = 0
def lwc_value(value):
    msg = PprzMessage('datalink', 'PAYLOAD_COMMAND')
    msg['ac_id']   = ac_id
    msg['command'] = [value]
    ivyInterface.send(msg)


def start_lace():
    append_lace()
    start_block(6)

