from .MissionBase import MissionBase

from ...common import messageInterface, PprzMessage
from .. import InsertMode

class Lace(MissionBase):

    """
    Lace 
    
    Mission type for the lace pattern. See MissionBase.py for more information.
    """
    
    parameterNames = ['start', 'first_turn_direction', 'circle_radius', 'drift']
    updatableNames = ['drift']

    def __init__(self, missionId, aircraftId, duration,
                       start, first_turn_direction, circle_radius, drift):

        super().__init__(missionId, aircraftId, duration)
        
        self.missionType                        = "Lace"
        self.parameters['start']                = start
        self.parameters['first_turn_direction'] = first_turn_direction
        self.parameters['circle_radius']        = circle_radius
        self.parameters['drift']                = drift


    def build_message(self, insertMode=InsertMode.Append):
        """Builds a ready to send paparazzi message from current parameters"""

        msg = PprzMessage('datalink', 'MISSION_CUSTOM')
        msg['ac_id']    = self.aircraftId
        msg['insert']   = insertMode
        msg['index']    = self.missionId
        msg['type']     = 'LACE'
        msg['duration'] = self.duration
        msg['params']   = [float(self['start'][0]),
                           float(self['start'][1]),
                           float(self['start'][2]),
                           float(self['first_turn_direction']),
                           float(self['circle_radius']),
                           float(self['drift'][0]),
                           float(self['drift'][1]),
                           float(self['drift'][2])]

        return msg

    
    # def build_update_messages(self, duration=-9.0, drift_x=None, drift_y=None, drift_z=None):
    #     """Builds (a) ready to send paparazzi message(s) for lace update"""

    #     msgs = []
    #     if drift_x is not None and drift_y is not None:
    #         msgs.append(PprzMessage('datalink', 'MISSION_UPDATE'))
    #         msgs[-1]['ac_id']    = self.aircraftId
    #         msgs[-1]['index']    = self.missionId
    #         msgs[-1]['duration'] = duration
    #         msgs[-1]['params']   = [drift_x, drift_y]
    #     if drift_z is not None:
    #         msgs.append(PprzMessage('datalink', 'MISSION_UPDATE'))
    #         msgs[-1]['ac_id']    = self.aircraftId
    #         msgs[-1]['index']    = self.missionId
    #         msgs[-1]['duration'] = duration
    #         msgs[-1]['params']   = [drift_z]
    #     return msgs



