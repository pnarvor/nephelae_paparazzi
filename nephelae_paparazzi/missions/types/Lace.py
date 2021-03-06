from .MissionBase import MissionBase

from ...common import messageInterface, PprzMessage
from .. import InsertMode

class Lace(MissionBase):

    """
    Lace 
    
    Mission type for the lace pattern. See MissionBase.py for more information.
    """
    
    parameterNames = ['start', 'first_turn_direction', 'circle_radius', 'drift']
    parameterTags  = {'start' : ['vector3d', 'position3d'],
                      'first_turn_direction' : ['scalar'],
                      'circle_radius'        : ['scalar'],
                      'drift' : ['vector3d', 'wind3d']}

    updatableNames = ['hdrift', 'zdrift']
    updatableTags  = {'hdrift' : ['vector2d', 'wind2d'],
                      'zdrift' : ['scalar',   'windz']}

    def __init__(self, missionId, aircraftId, insertMode, duration,
                       positionOffset=None, navFrame=None, pprzNavFrame=None,
                       start=None, first_turn_direction=None,
                       circle_radius=None, drift=None, updateRules={}):

        super().__init__(missionId, aircraftId, insertMode, duration,
                         positionOffset, navFrame, pprzNavFrame, updateRules)
        
        self.missionType                        = "Lace"
        self.parameters['start']                = start
        self.parameters['first_turn_direction'] = first_turn_direction
        self.parameters['circle_radius']        = circle_radius
        self.parameters['drift']                = drift


    def build_message(self):
        """Builds a ready to send paparazzi message from current parameters"""
        
        # Getting a partial message filled with parameters common to all
        # mission types.
        msg = super().build_message()
        
        msg['type']   = 'LACE'
        # Filling parameters specific to this mission type.
        # shifted with this specific aircraft NAVIGATION_REF
        msg['params'] = [float(self['start'][0]) + self.positionOffset[0],
                         float(self['start'][1]) + self.positionOffset[1],
                         float(self['start'][2]) + self.positionOffset[2],
                         float(self['first_turn_direction']),
                         float(self['circle_radius']),
                         float(self['drift'][0]),
                         float(self['drift'][1]),
                         float(self['drift'][2])]

        return msg

