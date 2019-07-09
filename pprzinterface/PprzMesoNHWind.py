import time
from netCDF4 import MFDataset

from nephelae_simulation.mesonh_interface import MesoNHVariable
from nephelae_simulation.mesonh_probe     import MesoNHCachedProbe

from .messages import Message
from .messages import WorldEnvReq
from .messages import WorldEnv


class PprzMesoNHWind:

    """PprzMesoNHWind

    Class for solely reading wind values in a MesoNH dataset for sending 
    wind feedback to a paparazzi simulated uav (identified by its executable
    pid shown in paparazzi requests). The feedback is going through
    paparazzi request system, using WORLD_ENV_REQ.

    This class is written is a very similar fashion to PprzMesoNHUav but could
    not have been part of it because it is not possible to associate paparazzi
    WORLD_ENV_REQ messages (indentified by a process pid) to a specific
    simulated UAV (user defined id).

    """


    def __init__(self, uavPid, navFrame, mesonhFiles,
                 targetCacheBounds=[[0,20],[-200,100],[-200,200],[-200,200]],
                 updateThreshold=0.25):

        self.uavPid   = uavPid
        self.navFrame = navFrame
        self.atm = MFDataset(mesonhFiles)
        self.probes = {}
        for var in ['UT','VT','WT']:
            mesoNHVar = MesoNHVariable(self.atm, var, interpolation='linear')
            self.probes[var] = MesoNHCachedProbe(mesoNHVar,
                                                 targetCacheBounds,
                                                 updateThreshold)
            self.probes[var].start()
        self.initialized = False
        self.stopping    = False
        self.stopped     = False

        self.reqBind = WorldEnvReq.bind(self.wind_request_callback, self.uavPid)


    def terminate(self):
        if self.reqBind is not None:
            self.stopping = True
            for i in range(50): # wait for 5s for stopping
            # for i in range(10): # wait for 1s for stopping
                if self.stopped or not self.initialized:
                    break
                time.sleep(0.1)
            Message.unbind(self.reqBind)
            self.reqBind = None
        for probe in self.probes.values():
            probe.stop()


    def wind_request_callback(self, msg):
       
        # /!\ In the WORLD_ENV_REQ message, utm position is given
        # relative to the navFrame (paparazzi NAVIGATION_REF message)

        t = msg.stamp - self.navFrame.stamp
        position = (t, msg.alt, msg.north, msg.east)
        if not self.initialized:
            for probe in self.probes.values():
                probe.request_cache_update(position, block=True)
            self.initialized = True
            return # return here because cache initialization could have been long

        values = []
        try:
            values.append(self.probes['UT'][position])
            values.append(self.probes['VT'][position])
            values.append(self.probes['WT'][position])
        except Exception as e:
            # raise e
            print("Could not read : ", e)
            print("Position : ", position)
            return # Not critical, no exception raised

        # print("Read : ", position, ", ", values, end="\n\n")
        
        if not self.stopping:
            response = WorldEnv.build(msg, values[0], values[1], values[2])
        else:
            # sending 0s for stopping wind
            response = WorldEnv.build(msg, 0.0, 0.0, 0.0)
            self.stopped = True
        # print("Response : ", response)
        response.send() 



