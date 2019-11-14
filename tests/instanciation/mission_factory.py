#! /usr/bin/python3

import sys
sys.path.append('../../')
import os
import signal
import time

# from nephelae_paparazzi.missions       import MissionManager, MissionFactory
# from nephelae_paparazzi.missions.rules import *
from nephelae_paparazzi.missions.builders import build_rule_set, build_mission_factory

parameterRules = {
    'start'                : [{'Length': [3]},
                              {'SimpleBounds':[[[-10000.0, -10000.0,  300.0], 
                                                [ 10000.0,  10000.0, 4000.0]]]}],
    'first_turn_direction' : [{'AllowedValues': [[-1.0, 1.0]]}],
    'circle_radius'        : [{'SimpleBounds':[[50.0, 500.0]]}],
    'drift'                : [{'Length': [3]},
                              {'SimpleBounds':[[[-10.0, -10.0, -5.0], [ 10.0,  10.0,  5.0]]]}]
}

lace_factory = build_mission_factory('Lace', parameterRules)
print(lace_factory)

