#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib import animation
import time

from ivy.std_api import *
import logging

from nephelae_paparazzi import PprzInterface

interface = PprzInterface()
interface.start()
signal.signal(signal.SIGINT, lambda sig,fr: interface.stop())
print("Waiting to catch drones...", end='')
time.sleep(5.0)
print("Go !")

plt.ion()

plots = {}
fig, axes = plt.subplots(1,1)
axes.set_xlim([-10, 200])
axes.set_ylim([-10, 200])
axes.set_aspect('equal')

while(interface.running):
    axes.clear()
    for uav in interface.uavs.keys():
    # for uav in [100]:
        xvalues = [pos.utm_east  - interface[uav].navFrame.utm_east  for pos in interface[uav].gps]
        yvalues = [pos.utm_north - interface[uav].navFrame.utm_north for pos in interface[uav].gps]
        plots[uav], = axes.plot(xvalues, yvalues, '.', label='uav_' + str(uav))
        # plots[uav], = axes.plot(xvalues, '.', label='uav_' + str(uav))
        fig.canvas.draw()
        fig.canvas.flush_events()
    # for uav in [100]:
    #     xvalues = [pos.utm_east  - interface[uav].navFrame.utm_east  for pos in interface[uav].gps]
    #     yvalues = [pos.utm_north - interface[uav].navFrame.utm_north for pos in interface[uav].gps]
    #     if not uav in plots.keys():
    #         plots[uav], = axes.plot(xvalues, yvalues, '.', label='uav_' + str(uav))
    #     else:
    #         plots[uav].set_xdata(xvalues)
    #         plots[uav].set_ydata(yvalues)
    #         fig.canvas.draw()
    #         fig.canvas.flush_events()
    time.sleep(0.5)


