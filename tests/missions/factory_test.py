#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.missions import MissionFactory
from nephelae_paparazzi.missions.rules import ParameterRules, SimpleBounds, TypeCheck, DefaultValue

laceFactory = MissionFactory("Lace", {
    'start_x'              : SimpleBounds([0.0, 1000.0], 'start_x'),
    'start_y'              : SimpleBounds([0.0, 1000.0], 'start_y'),
    'start_z'              : SimpleBounds([0.0, 1000.0], 'start_z'),
    'first_turn_direction' : TypeCheck((int,), 'first_turn_direction'),
    'circle_radius'        : SimpleBounds([50.0, 500.0], 'circle_radius'),
    'drift_x'              : SimpleBounds([-10.0, 10.0], 'drift_x'),
    'drift_y'              : SimpleBounds([-10.0, 10.0], 'drift_y'),
    'drift_z'              : ParameterRules([DefaultValue(7.2, 'drift_z'),
                                             SimpleBounds([-10.0, 10.0], 'drift_z')],
                                             'drift_z'),

})

# Should pass
lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                          start_x=0.0, start_y=0.0, start_z=0.0,
                          first_turn_direction=0, circle_radius=100.0,
                          drift_x=0.0, drift_y=0.0, drift_z=0.0)
print(lace0)
print("Task succeeded successfully")

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
except TypeError as e:
    print("Task failed successfully : ", e)

# Should pass
lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                          start_x=0.0, start_y=0.0, start_z=0.0,
                          first_turn_direction=0, circle_radius=100.0,
                          drift_x=0.0, drift_y=0.0, drift_z=None)
print(lace0)
print("Task succeeded successfully")


