from ivy.std_api import *
import logging

from netCDF4 import MFDataset

from nephelae_base.types import SensorSample

from nephelae_simulation.mesonh_interface import MesoNHVariable
from nephelae_simulation.mesonh_probe     import MesoNHCachedProbe

from . import messages as pmsg
from . import PprzUavBase

class PprzMesoNHUav(PprzUavBase):

    """PprzMesoNHUav

    Specialization of PprzUavBase intended to get sensor data from a MesoNH
    dataset. Sensor data are read in the MesoNH dataset and published to the
    sample subscribers each time a GPS message is received.

    """


    def __init__(self, uavId, navFrame,
                 mesonhFiles, mesonhVariables,
                 targetCacheBounds=[[0,20],[-200,100],[-200,200],[-200,200]],
                 updateThreshold=0.25):
        super().__init__(uavId, navFrame)

        self.atm = MFDataset(mesonhFiles)
        self.probes = {}
        for var in mesonhVariables:
            mesoNHVar = MesoNHVariable(self.atm, var, interpolation='linear')
            self.probes[var] = MesoNHCachedProbe(mesoNHVar,
                                                 targetCacheBounds,
                                                 updateThreshold)
            self.probes[var].start()
        self.initialized = False


    def terminate(self):
        super().terminate()
        for probe in self.probes.values():
            probe.stop()


    def gps_callback(self, msg):
        super().gps_callback(msg)

        position = msg - self.navFrame
        readKeys = (position.t, position.z, position.y, position.x)
        if not self.initialized:
            for probe in self.probes.values():
                probe.request_cache_update(readKeys, block=True)
            self.initialized = True
        
        for var in self.probes.keys():
            sample = SensorSample(variableName=var, producer=self.id,
                                   timeStamp=position.t,
                                   position=position,
                                   data=[self.probes[var][readKeys]])
            self.notify_sensor_sample(sample)




