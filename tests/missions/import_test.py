#! /usr/bin/python3

import sys
sys.path.append('../../')

from nephelae_paparazzi.missions.types import Lace


lace = Lace(missionId=1, aircraftId=200, duration=-1.0, 
            start=[1500.0, 900.0, 700.0],
            first_turn_direction=1.0, circle_radius=100.0,
            drift=[-7.0, -0.5, 0.0])

