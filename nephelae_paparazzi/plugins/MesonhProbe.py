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
        return [{'name'         : 'stop',
                 'method'       : MesonhProbe.stop,
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
                 'conflictMode' : 'abort'},
                {'name'         : 'rct_feedback',
                 'method'       : MesonhProbe.rct_feedback,
                 'conflictMode' : 'error'}
               ]


    def __initplugin__(self, mesonhFiles, mesonhVariables=[],
                       targetCacheBounds=[[0,20],[-500,500],[-500,500],[-400,200]],
                       updateThreshold=0.25, rctFeedback=True,
                       defaultRctBounds = Bounds(0.0, 1.0e-5),
                       mesonhOrigin=None):
        
        self.mesonhInitialized = False
        self.rctFeedback       = rctFeedback
        self.windFeedback       = rctFeedback
        self.add_notification_method('add_sample')

        # Check if proper variables are fetched to do the feedback
        if self.rctFeedback and 'RCT' not in mesonhVariables:
            mesonhVariables.append('RCT')

        if isinstance(mesonhFiles, MesonhDataset):
            self.atm = mesonhFiles
        else:
            self.atm = MesonhDataset(mesonhFiles)
        self.probes = {}
        for var in mesonhVariables:
            mesonhVar = MesonhVariable(self.atm, var,
                                       origin=mesonhOrigin,
                                       interpolation='linear')
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


    def stop(self):
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
                sample = SensorSample(variableName=var, producer=self.id,
                                      timeStamp=position.t,
                                      position=position,
                                      data=[value])
                self.add_sample(sample)

                if var == 'RCT' and self.rctFeedback:
                    self.rct_feedback(value)
            except Exception as e: # !!!!!!!!!!!!!! Fix this !
                print(traceback.format_exc())
                print("Could not read, feedback :", e)


    def add_sensor_observer(self, observer):
        self.attach_observer(observer, 'add_sample')


    def remove_sensor_observer(self, observer):
        self.detach_observer(observer, 'add_sample')


    def rct_feedback(self, rctValue):
        msg = PprzMessage('datalink', 'PAYLOAD_COMMAND')
        msg['ac_id']   = int(self.id)
        msg['command'] = [min(255,int(255 * rctValue / self.rctBounds.span()))]
        messageInterface.send(msg)



def build_mesonh_probe(aircraft, mesonhFiles, mesonhVariables=[],
                       targetCacheBounds=[[   0,  20],
                                          [-500, 500],
                                          [-500, 500],
                                          [-400, 200]],
                       updateThreshold=0.25, rctFeedback=True,
                       defaultRctBounds = Bounds(0.0, 1.0e-5),
                       mesonhOrigin=None):

    if isinstance(defaultRctBounds, list):
        defaultRctBounds = Bounds(defaultRctBounds[0],
                                  defaultRctBounds[-1])
    aircraft.load_plugin(MesonhProbe, mesonhFiles, mesonhVariables,
                         targetCacheBounds, updateThreshold, rctFeedback,
                         defaultRctBounds, mesonhOrigin)
