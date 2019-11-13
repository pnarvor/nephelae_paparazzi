from .MissionBase import MissionBase

from ...common import messageInterface, PprzMessage
from .. import InsertMode

class Lace(MissionBase):

    """
    Lace 
    
    Mission type for the lace pattern. See MissionBase.py for more information.
    """
    
    parameterNames = ['start', 'first_turn_direction', 'circle_radius', 'drift']
    updatableNames = ['hdrift', 'zdrift']

    def __init__(self, missionId, aircraftId, duration,
                       start, first_turn_direction, circle_radius, drift,
                       updateRules={}):

        super().__init__(missionId, aircraftId, duration)
        
        self.missionType                        = "Lace"
        self.parameters['start']                = start
        self.parameters['first_turn_direction'] = first_turn_direction
        self.parameters['circle_radius']        = circle_radius
        self.parameters['drift']                = drift
        self.updateRules                        = updateRules


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


    def build_update_message(self, duration=-9.0, hdrift=None, zdrift=None):
        """
        build a MISSION_UPDATE message for this mission

        /!\ Several parameters but wil build only one update message.
        Message will be build only for first non-None parameters, priority list
        is in this order : [hdrift, zdrift]
        
        Parameters
        ----------
        duration : float
            New duration for the mission. Set to -1.0 to set no limits and
            -9.0 to keep unchanged.
        """
        msg = PprzMessage('datalink', 'MISSION_UPDATE')
        msg['ac_id']    = self.aircraftId
        msg['index']    = self.missionId
        msg['duration'] = duration

        try:
            if hdrift is not None:
                self.updateRules['hdrift'].check(hdrift)
                msg['params'] = [hdrift[0], hdrift[1]]
                return msg

            elif zdrift is not None:
                self.updateRules['zdrift'].check(zdrift)
                msg['params'] = [zdrift]
                return msg

        except KeyError as e:
            print("No rules defined for update parameter '" + str(e.args[0]) +\
                  "'. Aborting. Feedback : " + str(e))


