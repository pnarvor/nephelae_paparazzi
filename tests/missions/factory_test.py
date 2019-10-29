#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.missions import MissionFactory
from nephelae_paparazzi.missions.rules import ParameterRules, SimpleBounds

laceFactory = MissionFactory("Lace", {
    'start_x'              : SimpleBounds('start_x', [0.0, 1000.0], 100),
    'start_y'              : SimpleBounds('start_y', [0.0, 1000.0], 101),
    'start_z'              : SimpleBounds('start_z', [0.0, 1000.0], 102),
    'first_turn_direction' : SimpleBounds('first_turn_direction', None, None),
    'circle_radius'        : SimpleBounds('circle_radius', [50.0, 500.0], 100.0),
    'drift_x'              : SimpleBounds('drift_x', [-10.0, 10.0], 7.5),
    'drift_y'              : SimpleBounds('drift_y', [-10.0, 10.0], 0.5),
    'drift_z'              : SimpleBounds('drift_z', [-10.0, 10.0], -5.0)
})

# Should instanciate
lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                          start_x=0.0, start_y=0.0, start_z=0.0,
                          first_turn_direction=0, circle_radius=100.0,
                          drift_x=0.0, drift_y=0.0, drift_z=0.0)

# Should fail
try:
    lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                              start_x=0.0, start_y=0.0, start_z=-1.0,
                              first_turn_direction=0, circle_radius=100.0,
                              drift_x=0.0, drift_y=0.0, drift_z=0.0)
except ValueError as e:
    print("Task failed successfully : ", e)

# Should fail
try:
    lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                              start_x=0.0, start_y=0.0, start_z=0.0,
                              first_turn_direction=None, circle_radius=100.0,
                              drift_x=0.0, drift_y=0.0, drift_z=0.0)
except ValueError as e:
    print("Task failed successfully : ", e)
