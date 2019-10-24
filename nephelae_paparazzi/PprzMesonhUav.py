import sys
import os
import traceback

from netCDF4 import MFDataset

from nephelae.types  import SensorSample, Bounds
from nephelae_mesonh import MesonhVariable, MesonhCachedProbe, MesonhDataset

from . import messages as pmsg
from .PprzUavBase import PprzUavBase

from ivy.std_api import *
import logging

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../')))
sys.path.append(PPRZ_HOME + "/var/lib/python")

# from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprzlink import messages_xml_map

def pprzlink_send(msg, sender_id=None):
    # copied from official pprzlink (to be fixed)
    if isinstance(msg, PprzMessage):
        if "telemetry" in msg.msg_class:
            if sender_id is None:
                print("ac_id needed to send telemetry message.")
                return None
            else:
                return IvySendMsg("%d %s %s" % (sender_id, msg.name, msg.payload_to_ivy_string()))
        else:
            if sender_id is None:
                return IvySendMsg("%s %s %s" % (msg.msg_class, msg.name, msg.payload_to_ivy_string()))
            else:
                return IvySendMsg("%s %s %s" % (str(sender_id), msg.name, msg.payload_to_ivy_string()))
    else:
        return IvySendMsg(msg)


class PprzMesonhUav(PprzUavBase):

    """PprzMesonhUav

    Specialization of PprzUavBase intended to get sensor data from a MesoNH
    dataset. Sensor data are read in the MesoNH dataset and published to the
    sample subscribers each time a GPS message is received.

    """

    defaultRctBounds = Bounds(0.0, 1.0e-5)

    def __init__(self, uavId, navFrame,
                 mesonhFiles, mesonhVariables,
                 targetCacheBounds=[[0,20],[-500,500],[-500,500],[-400,200]],
                 updateThreshold=0.25):
        # super().__init__(uavId, navFrame)
        
        if isinstance(mesonhFiles, MesonhDataset):
            self.atm = mesonhFiles
        else:
            self.atm = MesonhDataset(mesonhFiles)
        self.probes = {}
        for var in mesonhVariables:
            mesonhVar = MesonhVariable(self.atm, var, interpolation='linear')
            self.probes[str(var)] = MesonhCachedProbe(mesonhVar,
                                                 targetCacheBounds,
                                                 updateThreshold)
            self.probes[str(var)].start()
        self.initialized = False
        b = self.probes['RCT'].var.actual_range[0]
        if b.min is None or b.max is None:
            self.rctBounds = PprzMesonhUav.defaultRctBounds
            print("Warning. This Mesonh dataset does not seem to define " +
                  "the range of its RCT variable. Using default value.",
                  PprzMesonhUav.defaultRctBounds)
        else:
            self.rctBounds = Bounds(b[0], b[-1])

        # Mother class initialization at the end because it defines some ivy
        # callbacks, which could happend before end of init
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
                value = self.probes[var][readKeys]
                if var == 'RCT':
                    msg = PprzMessage('datalink', 'PAYLOAD_COMMAND')
                    msg['ac_id']   = int(self.id)
                    msg['command'] = [min(255,int(255 * value / self.rctBounds.span()))]
                    pprzlink_send(msg)
                sample = SensorSample(variableName=var, producer=self.id,
                                      timeStamp=position.t,
                                      position=position,
                                      data=[value])
                self.notify_sensor_sample(sample)
            except Exception as e:
                print(traceback.format_exc())
                print("Could not read, feedback :", e)




