from . import messages as pmsg

from .PprzInterface  import PprzInterface
from .PprzMesonhUav  import PprzMesonhUav
from .PprzMesonhWind import PprzMesonhWind


class PprzSimulation(PprzInterface):

    """PprzSimulation

    Class to manage simulated pprz Uavs flying in a MesoNH dataset
    Behavior similiar to PprzInterface but with added features related 
    mainly to wind simulation.

    """

    def __init__(self, mesonhFiles, mesonhVariables,
                 ivyIpp="127.255.255.255:2010",
                 windFeedback=True,
                 build_uav_callback=lambda uavId, navRef: PprzMesonhUav(uavId,
                                                                        navRef,
                                                                        mesonhFiles, 
                                                                        mesonhVariables)):
        super().__init__(ivyIpp, build_uav_callback)
        
        self.mesonhFiles  = mesonhFiles
        self.windFeedback = windFeedback
        self.windProbes   = {}
        self.windIvyBind  = None

    
    def start(self):
        super().start()
        if self.windFeedback:
            self.enable_wind_feedback()
        

    def stop(self):
        self.disable_wind_feedback()
        super().stop()


    def enable_wind_feedback(self):
        if self.windIvyBind is None:
            self.windIvyBind = pmsg.WorldEnvReq.bind(self.worldenvreq_callback)


    def disable_wind_feedback(self):
        if self.windIvyBind is not None:
            pmsg.Message.unbind(self.windIvyBind)
            self.windIvyBind = None
            for probe in self.windProbes.values():
                probe.terminate()
            self.windProbes = {}


    def worldenvreq_callback(self, msg):
        senderPid = msg.sender_pid()
        if senderPid not in self.windProbes.keys():
            self.windProbes[senderPid] = PprzMesonhWind(senderPid,
                                                        self.navFrame,
                                                        self.mesonhFiles)
