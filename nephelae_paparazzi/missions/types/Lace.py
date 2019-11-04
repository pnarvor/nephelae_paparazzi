from .MissionBase import MissionBase

from ...common import messageInterface, PprzMessage
from .. import InsertMode

class Lace(MissionBase):

    """
    Lace 
    
    Mission type for the lace pattern. See MissionBase.py for more information.
    """
    
    parameterNames = ['start_x', 'start_y', 'start_z',
                      'first_turn_direction', 'circle_radius',
                      'drift_x', 'drift_y', 'drift_z']
    updatableNames = ['drift_x', 'drift_y', 'drift_z']

    def __init__(self, missionId, aircraftId, duration,
                       start_x, start_y, start_z, first_turn_direction,
                       circle_radius, drift_x, drift_y, drift_z):
        super().__init__(missionId, aircraftId, duration)
        
        self.missionType                        = "Lace"
        self.parameters['start_x']              = float(start_x)
        self.parameters['start_y']              = float(start_y)
        self.parameters['start_z']              = float(start_z)
        self.parameters['first_turn_direction'] = int(first_turn_direction)
        self.parameters['circle_radius']        = float(circle_radius)
        self.parameters['drift_x']              = float(drift_x)
        self.parameters['drift_y']              = float(drift_y)
        self.parameters['drift_z']              = float(drift_z)


    def build_message(self, insertMode=InsertMode.Append):
        """Builds a ready to send paparazzi message from current parameters"""

        msg = PprzMessage('datalink', 'MISSION_CUSTOM')
        msg['ac_id']    = self.aircraftId
        msg['insert']   = insertMode
        msg['index']    = self.missionId
        msg['type']     = 'LACE'
        msg['duration'] = self.duration
        msg['params']   = [self['start_x'], self['start_y'], self['start_z'],
                           self['first_turn_direction'], self['circle_radius'],
                           self['drift_x'], self['drift_y'], self['drift_z']]

        return msg

    
    def build_update_messages(self, duration=-9.0, drift_x=None, drift_y=None, drift_z=None):
        """Builds (a) ready to send paparazzi message(s) for lace update"""

        msgs = []
        if drift_x is not None and drift_y is not None:
            msgs.append(PprzMessage('datalink', 'MISSION_UPDATE'))
            msgs[-1]['ac_id']    = self.aircraftId
            msgs[-1]['index']    = self.missionId
            msgs[-1]['duration'] = duration
            msgs[-1]['params']   = [drift_x, drift_y]
        if drift_z is not None:
            msgs.append(PprzMessage('datalink', 'MISSION_UPDATE'))
            msgs[-1]['ac_id']    = self.aircraftId
            msgs[-1]['index']    = self.missionId
            msgs[-1]['duration'] = duration
            msgs[-1]['params']   = [drift_z]
        return msgs



