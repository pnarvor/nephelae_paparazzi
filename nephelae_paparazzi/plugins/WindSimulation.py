from nephelae_mesonh import MesonhDataset

from ..PprzMesonhWind import PprzMesonhWind
from ..messages       import Message, WorldEnvReq

class WindSimulation:

    """
    WindSimulation

    Plugin for nephelae_scenario.Scenario to manage wind feedback from mesonh
    to the flying aircrafts (specifically simulated flight in wind).
    """

    def __pluginmethods__():
        return [{'name'         : 'start',
                 'method'       : WindSimulation.start,
                 'conflictMode' : 'append'},
                {'name'         : 'stop',
                 'method'       : WindSimulation.stop,
                 'conflictMode' : 'prepend'},
                {'name'         : 'worldenvreq_callback',
                 'method'       : WindSimulation.worldenvreq_callback,
                 'conflictMode' : 'prepend'}
               ]

    def __initplugin__(self, mesonhFiles):

        if isinstance(mesonhFiles, MesonhDataset):
            self.atm = mesonhFiles
        else:
            self.atm = MesonhDataset(mesonhFiles)
        self.windProbes   = {}
        self.windIvyBind  = None

    
    def start(self):
        if self.windIvyBind is None:
            self.windIvyBind = WorldEnvReq.bind(self.worldenvreq_callback)
        

    def stop(self):
        if self.windIvyBind is not None:
            Message.unbind(self.windIvyBind)
            self.windIvyBind = None
            for probe in self.windProbes.values():
                probe.terminate()
            self.windProbes = {}


    def worldenvreq_callback(self, msg):
        senderPid = msg.sender_pid()
        if senderPid not in self.windProbes.keys():
            self.windProbes[senderPid] = PprzMesonhWind(senderPid,
                                                        self.localFrame,
                                                        self.atm)



