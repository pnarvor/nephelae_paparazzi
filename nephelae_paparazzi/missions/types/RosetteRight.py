from .MissionBase import MissionBase

from ...common import messageInterface, PprzMessage
from .. import InsertMode

class RosetteRight(MissionBase):

    """
    Rosette
    
    Mission type for the rosette pattern. See MissionBase.py for more information.
    """
    
    parameterNames = ['start', 'circle_radius', 'drift']
    parameterTags  = {'start' : ['vector3d', 'position3d'],
                      'circle_radius'        : ['scalar'],
                      'drift' : ['vector3d', 'wind3d']}

    updatableNames = ['hdrift', 'zdrift', 'center']
    updatableTags  = {'hdrift' : ['vector2d', 'wind2d'],
                      'zdrift' : ['scalar',   'windx']}

    def __init__(self, missionId, aircraftId, insertMode, duration,
                       start, circle_radius, drift,
                       updateRules={}):

        super().__init__(missionId, aircraftId,
                         insertMode, duration, updateRules)
        
        self.missionType                        = "Rosette"
        self.parameters['start']                = start
        self.parameters['circle_radius']        = circle_radius
        self.parameters['drift']                = drift


    def build_message(self, pprzNavRef=None):
        """Builds a ready to send paparazzi message from current parameters"""
        
        # Getting a partial message filled with parameters common to all
        # mission types.
        msg = super().build_message()

        # Filling parameters specific to this mission type.
        msg['type']   = 'RSTT'
        if pprzNavRef is None:
            # Filling parameters specific to this mission type.
            msg['params'] = [float(self['start'][0]),
                             float(self['start'][1]),
                             float(self['start'][2]),
                             1.0,
                             float(self['circle_radius']),
                             float(self['drift'][0]),
                             float(self['drift'][1]),
                             float(self['drift'][2])]
        else:
            # Filling parameters specific to this mission type.
            # shifted with this specific aircraft NAVIGATION_REF
            msg['params'] = [float(self['start'][0]),
                             float(self['start'][1]),
                             float(self['start'][2] - pprzNavRef['ground_alt']),
                             1.0,
                             float(self['circle_radius']),
                             float(self['drift'][0]),
                             float(self['drift'][1]),
                             float(self['drift'][2])]

        return msg

