from .MissionBase import MissionBase

from ...common import messageInterface, PprzMessage
from .. import InsertMode

class Rosette(MissionBase):

    """
    Rosette
    
    Mission type for the rosette pattern. See MissionBase.py for more information.
    """
    
    parameterNames = ['start', 'first_turn_direction', 'circle_radius', 'drift']
    updatableNames = ['hdrift', 'zdrift', 'center']

    def __init__(self, missionId, aircraftId, duration,
                       start, first_turn_direction, circle_radius, drift,
                       updateRules={}):

        super().__init__(missionId, aircraftId, duration, updateRules)
        
        self.missionType                        = "Rosette"
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
        msg['type']     = 'RSTT'
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

