from .MissionBase import MissionBase

from ...common import messageInterface, PprzMessage
from .. import InsertMode

class Spiral3D(MissionBase):

    """
    Spiral3D
    
    Mission type for the spiral3D pattern. See MissionBase.py for more information.
    """
    
    parameterNames = ['start', 'alt_stop', 'radius_start', 'radius_stop', 'drift']
    parameterTags  = {'start'        : ['vector3d', 'position3d'],
                      'alt_stop'     : ['scalar', 'positionz'],
                      'radius_start' : ['scalar'],
                      'radius_stop'  : ['scalar'],
                      'drift'        : ['vector3d', 'wind3d']}

    updatableNames = ['hdrift', 'zdrift']
    updatableTags  = {'hdrift' : ['vector2d', 'wind2d'],
                      'zdrift' : ['scalar',   'windz']}

    def __init__(self, missionId, aircraftId, insertMode, duration,
                       start, alt_stop, radius_start, radius_stop, drift,
                       updateRules={}):

        super().__init__(missionId, aircraftId,
                         insertMode, duration, updateRules)
        
        self.missionType                = "Spiral3D"
        self.parameters['start']        = start
        self.parameters['alt_stop']     = alt_stop
        self.parameters['radius_start'] = radius_start
        self.parameters['radius_stop']  = radius_stop
        self.parameters['drift']        = drift


    def build_message(self):
        """Builds a ready to send paparazzi message from current parameters"""
        
        # Getting a partial message filled with parameters common to all
        # mission types.
        msg = super().build_message()

        # Filling parameters specific to this mission type.
        msg['type']   = 'SPIR3'
        msg['params'] = [float(self['start'][0]),
                         float(self['start'][1]),
                         float(self['start'][2]),
                         float(self['alt_stop']),
                         float(self['radius_start']),
                         float(self['radius_stop']),
                         float(self['drift'][0]),
                         float(self['drift'][1]),
                         float(self['drift'][2])]

        return msg

