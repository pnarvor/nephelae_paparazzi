import sys
import os
import traceback

from . import messages as pmsg
from .PprzUavBase import PprzUavBase
from .missions import MissionManager



class PprzMissionUav(PprzUavBase):

    """PprzMissionUav

    Specialization of PprzUavBase intended to get sensor data from a MesoNH
    dataset. Sensor data are read in the MesoNH dataset and published to the
    sample subscribers each time a GPS message is received.

    """

    def __init__(self, uavId, navFrame, missionFactories=[]):
        

        # Mother class initialization at the end because it defines some ivy
        # callbacks, which could happend before end of init
        factories = {}
        for factory in missionFactories:
            factories[factory.missionType] = factory
        self.missionManager = MissionManager(uavId, factories=factories)
        super().__init__(uavId, navFrame)


    def terminate(self):
        super().terminate()
        for probe in self.probes.values():
            probe.stop()




