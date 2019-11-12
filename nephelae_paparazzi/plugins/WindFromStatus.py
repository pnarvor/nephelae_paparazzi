import traceback
import numpy as np

from nephelae.types  import SensorSample, Bounds

from ..common import messageInterface, PprzMessage


class WindFromStatus:

    """
    WindFromStatus

    Aircraft plugin to get data from a MesonhFile and send a LWC feedback
    to the aircraft.
    """

    def __pluginmethods__():
        return [{'name'         : 'flight_param_callback',
                 'method'       : WindFromStatus.wind_estimate,
                 'conflictMode' : 'append'}
               ]


    def __initplugin__(self):
        if not hasattr(self, 'add_sample'):
            self.add_notification_method('add_sample')
        # self.attach_observer(self, 'add_sample')


    def wind_estimate(self, flightParam):
        print("Wind estimation")

        # Angles are given relative to north, in degrees, and clock-wise...
        heading = -np.pi*(float(self.status.heading) - 90.0)/ 180.0
        course  = -np.pi*(float(self.status.course ) - 90.0)/ 180.0

        vsol = float(self.status.speed) * \
               np.array([np.cos(course), np.sin(course)])
        vair = float(self.status.air_speed) * \
               np.array([np.cos(heading), np.sin(heading)])
        wind = vsol - vair

        print(np.linalg.norm(wind))

        self.add_sample(SensorSample(variableName='wind',
                                     producer=self.id,
                                     timeStamp=self.status.position.t,
                                     position=self.status.position,
                                     data=[wind]))
        
        
