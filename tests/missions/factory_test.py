#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.missions import MissionFactory
from nephelae_paparazzi.missions.rules import ParameterRules, SimpleBounds, TypeCheck, DefaultValue, AllowedValues, Length

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

print(laceFactory.parameter_rules_summary())

# Should pass
lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                          start=[0.0, 0.0, 400.0],
                          first_turn_direction=1.0, circle_radius=100.0,
                          drift=[0.0, 0.0, 0.0])
print(lace0)
print("Task succeeded successfully")

# Should fail
try:
    lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                              start=[0.0, 0.0, 200.0],
                              first_turn_direction=1.0, circle_radius=100.0,
                              drift=[0.0, 0.0, 0.0])
except ValueError as e:
    print("Task failed successfully : ", e)

try:
    lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                              start=[-12000.0, 0.0, 300.0],
                              first_turn_direction=1.0, circle_radius=100.0,
                              drift=[0.0, 0.0, 0.0])
except ValueError as e:
    print("Task failed successfully : ", e)

# Should fail
try:
    lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                              start=[0.0, 0.0, 400.0],
                              first_turn_direction=0.0, circle_radius=100.0,
                              drift=[0.0, 0.0, 0.0])
except ValueError as e:
    print("Task failed successfully : ", e)

# # Should pass
# lace0 = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
#                           start_x=0.0, start_y=0.0, start_z=0.0,
#                           first_turn_direction=1.0, circle_radius=100.0,
#                           drift_x=0.0, drift_y=0.0, drift_z=None)
# print(lace0)
# print("Task succeeded successfully")


