#! /usr/bin/python3

import signal

from nephelae_paparazzi import MessageInterface

messageInterface = MessageInterface()

def callback(msg):
    # print(msg)
    print(msg.fieldvalues)

# bindId = messageInterface.bind(callback, '(.* GPS .*)')
# bindId = messageInterface.bind(callback, '(.* FLIGHT_PARAM .*)')
# bindId = messageInterface.bind(callback, '(.* NAVIGATION_REF .*)')
# bindId = messageInterface.bind(callback, '(.* AP_STATUS .*)')
# bindId = messageInterface.bind(callback, '(.* NAV_STATUS .*)')
# bindId = messageInterface.bind(callback, '(.* MISSION_STATUS .*)')
bindId = messageInterface.bind(callback, '(.* BAT .*)')
