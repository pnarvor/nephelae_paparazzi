#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.missions.types import Lace


lace = Lace(missionId=1, aircraftId=200, duration=-1.0, 
            start_x=1500.0, start_y=900.0, start_z=700.0,
            first_turn_direction=0, circle_radius=50.0, 
            drift_x=-7.0, drift_y=-0.5, drift_z=3.0)

