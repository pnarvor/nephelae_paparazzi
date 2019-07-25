#! /usr/bin/python3

import sys
sys.path.append('../../')
import os
import signal
import time
import argparse

import nephelae_paparazzi.pprzinterface as ppint

defaultMesonhFile = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc'
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mesonh-files", nargs='*',
					default=defaultMesonhFile,
                    help="MesoNH files to fly the simulated UAV into")
args = parser.parse_args()

def build_uav(uavId, navRef):
    uav = ppint.PprzMesoNHUav(uavId, navRef, args.mesonh_files, ['RCT', 'WT'])
    return uav

interface = ppint.PprzSimulation(args.mesonh_files, [],
                                 build_uav_callback=build_uav)
interface.start()


def stop():
    if interface.running:
        print("Shutting down... (can take a few seconds) ", end='')
        sys.stdout.flush()
        interface.stop()
        print("Complete.")
signal.signal(signal.SIGINT, lambda sig,fr: stop())

