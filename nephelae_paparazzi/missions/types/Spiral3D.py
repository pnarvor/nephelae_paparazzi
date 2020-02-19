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
                       positionOffset=None, navFrame=None, pprzNavFrame=None,
                       start=None, alt_stop=None, radius_start=None,
                       radius_stop=None, drift=None, updateRules={}):

        super().__init__(missionId, aircraftId, insertMode, duration,
                         positionOffset, navFrame, pprzNavFrame, updateRules)
        
        self.missionType                = "Spiral3D"
        self.parameters['start']        = start
        self.parameters['alt_stop']     = alt_stop
        self.parameters['radius_start'] = radius_start
        self.parameters['radius_stop']  = radius_stop
        self.parameters['drift']        = drift
        
        # Spiral3D have not the same reference frame as the other missions.
        if positionOffset is None:
            if navFrame is None or pprzNavFrame is None:
                raise ValueError("You have to give either a positionOffset" +
                                 " of both navFrame and pprzNavFrame.")
            self.positionOffset = [
                navFrame.position.x - self.pprzNavFrame.utm_east,
                navFrame.position.y - self.pprzNavFrame.utm_north,
                navFrame.position.z]
        else:
            self.positionOffset = positionOffset
        print("Position offset for mission", self.missionType, ":", self.positionOffset)


    def build_message(self, pprzNavRef=None, localRef=None):
        """Builds a ready to send paparazzi message from current parameters"""
        
        # Getting a partial message filled with parameters common to all
        # mission types.
        msg = super().build_message()

        # Filling parameters specific to this mission type.
        msg['type']   = 'SPIR3'
        # Filling parameters specific to this mission type.
        # shifted with this specific aircraft NAVIGATION_REF
        msg['params'] = [float(self['start'][0]) + self.positionOffset[0],
                         float(self['start'][1]) + self.positionOffset[1],
                         float(self['start'][2]) + self.positionOffset[2],
                         float(self['alt_stop']) + self.positionOffset[2],
                         float(self['radius_start']),
                         float(self['radius_stop']),
                         float(self['drift'][0]),
                         float(self['drift'][1]),
                         float(self['drift'][2])]
        return msg

