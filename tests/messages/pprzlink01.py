#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.common import messageInterface, PprzMessage

def callback(senderId, msg):
    print(senderId)
    print(msg)

messageInterface.subscribe(callback, '(200 GPS .*)')
