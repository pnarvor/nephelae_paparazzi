import sys
import os
import traceback

from ivy.std_api import *
import logging

from netCDF4 import MFDataset

from nephelae.types  import SensorSample
from nephelae_mesonh import MesonhVariable
from nephelae_mesonh import MesonhCachedProbe

from . import messages as pmsg
from .PprzUavBase import PprzUavBase

class PprzMesonhUav(PprzUavBase):

    """PprzMesonhUav

    Specialization of PprzUavBase intended to get sensor data from a MesoNH
    dataset. Sensor data are read in the MesoNH dataset and published to the
    sample subscribers each time a GPS message is received.

    """


    def __init__(self, uavId, navFrame,
                 mesonhFiles, mesonhVariables,
                 targetCacheBounds=[[0,20],[-500,500],[-500,500],[-400,200]],
                 updateThreshold=0.25):
        # Bad, callback can happend before end of init
        # super().__init__(uavId, navFrame)
        
        if isinstance(mesonhFiles, MFDataset):
            self.atm = mesonhFiles
        else:
            self.atm = MFDataset(mesonhFiles)
        self.probes = {}
        for var in mesonhVariables:
            mesonhVar = MesonhVariable(self.atm, var, interpolation='linear')
            self.probes[str(var)] = MesonhCachedProbe(mesonhVar,
                                                 targetCacheBounds,
                                                 updateThreshold)
            self.probes[str(var)].start()
        self.initialized = False
        super().__init__(uavId, navFrame)


    def terminate(self):
        super().terminate()
        for probe in self.probes.values():
            probe.stop()


    def gps_callback(self, msg):
        super().gps_callback(msg)

        position = msg - self.navFrame
        readKeys = (position.t, position.x, position.y, position.z)
        if not self.initialized:
            for probe in self.probes.values():
                probe.request_cache_update(readKeys, block=True)
            self.initialized = True
        
        for var in self.probes.keys():
            try:
                sample = SensorSample(variableName=var, producer=self.id,
                                      timeStamp=position.t,
                                      position=position,
                                      data=[self.probes[var][readKeys]])
                self.notify_sensor_sample(sample)
            except Exception as e:
                print(traceback.format_exc())
                print("Could not read, feedback :", e)




