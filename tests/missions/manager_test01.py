#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.missions import MissionFactory, MissionManager
from nephelae_paparazzi.missions.rules import ParameterRules, SimpleBounds, AllowedValues, DefaultValue, Length
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
    'start'                : [SimpleBounds([[-10000.0, -10000.0,  300.0],
                                            [ 10000.0,  10000.0, 4000.0]],'start'),
                              Length(3, 'start')],
    'first_turn_direction' : AllowedValues([-1.0, 1.0], 'first_turn_direction'),
    'circle_radius'        : SimpleBounds([50.0, 500.0], 'circle_radius'),
    'drift'                : [SimpleBounds([[-10.0, -10.0, -5.0],
                                            [ 10.0,  10.0,  5.0]],'drift'),
                              Length(3, 'drift')],
})

manager = MissionManager("200", factories={"Lace":laceFactory})
print(manager.mission_parameter_rules('Lace'))

# should fail
try:
    manager = MissionManager("200", factories={"Lace":laceFactory})
except ValueError as e:
    print("Task failed successfully. Feedback :", e)

manager.create_mission('Lace', duration=-1,
                       start=[1500.0, 900.0, 700.0],
                       first_turn_direction=1.0, circle_radius=100.0,
                       drift=[-7.0, -0.5, 0.0])
print(manager.pendingMissions[0])






