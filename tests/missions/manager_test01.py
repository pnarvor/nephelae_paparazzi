#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.missions import MissionFactory, MissionManager
from nephelae_paparazzi.missions.rules import ParameterRules, SimpleBounds, TypeCheck, DefaultValue
from nephelae_paparazzi.common import messageInterface, PprzMessage

def send_lwc(ac_id, value):
    msg = PprzMessage('datalink', 'PAYLOAD_COMMAND')
    msg['ac_id']   = ac_id
    msg['command'] = [value]
    messageInterface.send(msg)

def start_block(ac_id, index):
    msg = PprzMessage('ground', 'JUMP_TO_BLOCK')
    msg['block_id'] = index
    msg['ac_id'] = ac_id
    messageInterface.send(msg)

def next_mission(ac_id):
    msg = PprzMessage('datalink', 'NEXT_MISSION')
    msg['ac_id'] = ac_id
    messageInterface.send(msg)

laceFactory = MissionFactory("Lace", {
    'start_x'              : SimpleBounds([-10000.0, 10000.0], 'start_x'),
    'start_y'              : SimpleBounds([-10000.0, 10000.0], 'start_y'),
    'start_z'              : SimpleBounds([300.0, 4000.0], 'start_z'),
    'first_turn_direction' : TypeCheck((int,), 'first_turn_direction'),
    'circle_radius'        : SimpleBounds([50.0, 500.0], 'circle_radius'),
    'drift_x'              : SimpleBounds([-10.0, 10.0], 'drift_x'),
    'drift_y'              : SimpleBounds([-10.0, 10.0], 'drift_y'),
    'drift_z'              : ParameterRules([DefaultValue(7.2, 'drift_z'),
                                             SimpleBounds([-10.0, 10.0], 'drift_z')],
                                             'drift_z'),

})

manager = MissionManager("200", factories={"Lace":laceFactory})
# should fail
try:
    manager = MissionManager("200", factories={"Lace":laceFactory})
except ValueError as e:
    print("Task failed successfully. Feedback :", e)

manager.create_mission('Lace', duration=-1,
                       start_x=1500.0, start_y=900.0, start_z=700.0,
                       first_turn_direction=0, circle_radius=80.0,
                       drift_x=-7.0, drift_y=-0.5, drift_z=0.0)






