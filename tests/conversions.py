#! /usr/bin/python3

import sys
sys.path.append('../')

from nephelae_paparazzi.messages import Gps
from nephelae_paparazzi.messages import NavigationRef

import nephelae.types as ntypes

refMsg = NavigationRef("100 NAVIGATION_REF 360285 4813595 31 185.000000")
gpsMsg = Gps("100 GPS 3 36037349 481362656 2390 253320 1278 21 0 207906480 31 0")

gps = gpsMsg.to_base_type()
ref = refMsg.to_base_type()
print(gps)
print(ref)

