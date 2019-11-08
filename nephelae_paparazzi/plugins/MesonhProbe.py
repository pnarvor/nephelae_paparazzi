import traceback

from nephelae.types  import SensorSample, Bounds
from nephelae_mesonh import MesonhVariable, MesonhCachedProbe, MesonhDataset

from ..common import messageInterface, PprzMessage


class MesonhProbe:

    """
    MesonhProbe

    Aircraft plugin to get data from a MesonhFile and send a LWC feedback
    to the aircraft.
    """

    def __pluginmethods__():
        return [{'name'         : 'terminate',
                 'method'       : MesonhProbe.terminate,
                 'conflictMode' : 'prepend'},
                {'name'         : 'gps_callback',
                 'method'       : MesonhProbe.gps_callback,
                 'conflictMode' : 'append'},
                {'name'         : 'gps_callback',
                 'method'       : MesonhProbe.gps_callback,
                 'conflictMode' : 'append'},
                {'name'         : 'add_sensor_observer',
                 'method'       : MesonhProbe.add_sensor_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'remove_sensor_observer',
                 'method'       : MesonhProbe.remove_sensor_observer,
                 'conflictMode' : 'abort'}
               ]


    def __initplugin__(self, mesonhFiles, mesonhVariables,
                       targetCacheBounds=[[0,20],[-500,500],[-500,500],[-400,200]],
                       updateThreshold=0.25, rctFeedback=True,
                       defaultRctBounds = Bounds(0.0, 1.0e-5)):
        
        self.mesonhInitialized = False
        self.rctFeedback       = rctFeedback
        self.add_notification_method('add_sample')

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

        b = self.probes['RCT'].var.actual_range[0]
        if b.min is None or b.max is None:
            self.rctBounds = defaultRctBounds
            print("Warning. This Mesonh dataset does not seem to define " +
                  "the range of its RCT variable. Using default value.",
                  defaultRctBounds)
        else:
            self.rctBounds = Bounds(b[0], b[-1])


    def terminate(self):
        for probe in self.probes.values():
            probe.stop()


    def gps_callback(self, msg):

        position = msg - self.navFrame
        readKeys = (position.t, position.x, position.y, position.z)
        if not self.mesonhInitialized:
            for probe in self.probes.values():
                probe.request_cache_update(readKeys, block=True)
            self.mesonhInitialized = True
        
        for var in self.probes.keys():
            try:
                value = self.probes[var][readKeys]
                if var == 'RCT' and self.rctFeedback:
                    msg = PprzMessage('datalink', 'PAYLOAD_COMMAND')
                    msg['ac_id']   = int(self.id)
                    msg['command'] = [min(255,int(255 * value / self.rctBounds.span()))]
                    messageInterface.send(msg)
                sample = SensorSample(variableName=var, producer=self.id,
                                      timeStamp=position.t,
                                      position=position,
                                      data=[value])
                self.add_sample(sample)
            except Exception as e:
                print(traceback.format_exc())
                print("Could not read, feedback :", e)


    def add_sensor_observer(self, observer):
        self.attach_observer(observer, 'add_sample')


    def remove_sensor_observer(self, observer):
        self.detach_observer(observer, 'add_sample')

