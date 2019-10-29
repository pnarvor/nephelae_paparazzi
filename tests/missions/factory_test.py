#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.missions import MissionFactory

laceFactory = MissionFactory("Lace", {})

lace = laceFactory.build(missionId=1, aircraftId=200, duration=-1.0,
                         start_x=0.0, start_y=0.0, start_z=0.0,
                         first_turn_direction=0, circle_radius=100.0,
                         drift_x=0.0, drift_y=0.0, drift_z=0.0)



