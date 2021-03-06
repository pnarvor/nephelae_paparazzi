# from . import missionTypes
from ...common import PprzMessage

class MissionBase:
    """
    MissionBase

    Base mission type for all mission instances.
    Holds all common attributes such as aircraft id, duration, index...

    class Attributes
    ----------------
    parameterNames : list(str, ...)
        List of parameters names for a mission specific parameters.

    parameterTags : dict(str:list(str,...), ...)
        Each element contains a list of tags to describe the nature of the
        parameter in a high level fashion (for example in a mission lace, the
        'start' parameter represent a 3D position, so get the tag
        'position_3D'. Each parameter can have multiple tags.
        The keys of the dictionary are the parameterNames.

    updatableNames : list(str, ...)
        List of parameters names which can be updated. Can be a subset of
        parameterNames or include other parameters.

    updatableTags : dict(str:list(str,...), ...)
        Similar to parameterTags, but for updatables parameters


    Attributes
    ----------
    missionId : int
        Unique index of the mission in the aircraft. Is exactly equal to the
        index indicated by the MISSION_STATUS message.

    aircraftId : int
        Paparazzi aircraft id. Aircraft to which this mission is associated.

    duration : float (in seconds)
        Mission duration.
        /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
        Must this represent time left in the mission or total time of
        the mission ?
        /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\

    parameters : dict('str':AnyType, ...)
        Additional parameters to be filed by subclasses.
    """
    parameterNames      = []
    parameterAttributes = {}
    updatableNames      = []
    updatableTags       = []

    def __init__(self, missionId, aircraftId, insertMode, duration,
                 positionOffset=None, navFrame=None, pprzNavFrame=None,
                 updateRules={}):
        
        self.missionType  = None
        self.missionId    = int(missionId)
        self.aircraftId   = int(aircraftId)
        self.insertMode   = insertMode
        self.duration     = float(duration)
        self.parameters   = {}
        self.updateRules  = updateRules
        self.authorized   = False

        if positionOffset is None:
            if navFrame is None or pprzNavFrame is None:
                raise ValueError("You have to give either a positionOffset" +
                                 " of both navFrame and pprzNavFrame.")
            self.positionOffset = [
                navFrame.position.x - pprzNavFrame.utm_east,
                navFrame.position.y - pprzNavFrame.utm_north,
                navFrame.position.z - pprzNavFrame.ground_alt]
        else:
            self.positionOffset = positionOffset
        print("Position offset for mission", self.missionType, ":", self.positionOffset)
        
    def __str__(self):
        prefix = "\n  "
        maxWidth = max([len(w) for w in
                       ["aircraftId"] + list(self.parameters.keys())])
        res = "Mission " + str(self.missionType) +\
              prefix + "missionId".ljust(maxWidth)  + " : " + str(self.missionId) +\
              prefix + "aircraftId".ljust(maxWidth) + " : " + str(self.aircraftId) +\
              prefix + "insertMode".ljust(maxWidth) + " : " + str(self.insertMode) +\
              prefix + "duration".ljust(maxWidth)   + " : " + str(self.duration)
        for key in self.__class__.parameterNames:
            res = res + prefix + key.ljust(maxWidth) + " : " + str(self[key])
        return res


    def __getitem__(self, key):
        """Simple helper to shorten parameter acces"""

        if key == "missionType":
            return self.missionType
        elif key == "missionId":
            return self.missionId
        elif key == "aircraftId":
            return self.aircraftId
        elif key == "insertMode":
            return self.insertMode
        elif key == "duration":
            return self.duration
        else:
            return self.parameters[key]


    def to_dict(self):
        return {'type'           : self.missionType,
                'missionId'      : self.missionId,
                'aircraftId'     : self.aircraftId,
                'insertMode'     : self.insertMode,
                'duration'       : self.duration,
                'positionOffset' : self.positionOffset,
                'parameters'     : self.parameters,
                'authorized'     : self.authorized
                }


    def build_message(self):
        """
        build_message
        
        Builds a MISSION_CUSTOM Paparazzi message, filling only parameters
        common to all mission types. Other parameters must be filled in
        MissionBase specializations.

        Returns a partially filled PprzMessage
        """

        msg = PprzMessage('datalink', 'MISSION_CUSTOM')
        msg['ac_id']    = self.aircraftId
        msg['insert']   = self.insertMode
        msg['index']    = self.missionId
        msg['duration'] = self.duration

        return msg


    def build_update_messages(self, duration=-9.0, **params):
        """
        Builds MISSION_UPDATE messages for this mission.
        
        Will return a list of messages even with only one element to update.

        Parameters
        ----------
        duration : float
            New duration for the mission. Set to -1.0 to set no limits and
            -9.0 to keep unchanged.
        """

        res = []
        for paramName in params.keys():
            msg = PprzMessage('datalink', 'MISSION_UPDATE')
            msg['ac_id']    = self.aircraftId
            msg['index']    = self.missionId
            msg['duration'] = duration

            try:
                param = self.updateRules[paramName].check(params[paramName])
            except KeyError as e:
                print("No rules defined for update parameter '" + str(e.args[0]) +\
                      "'. Aborting. Exception feedback : " + str(e))

            # param can be a multidimensionnal parameter but msg['params']
            # expects a list of floats
            if hasattr(param, '__getitem__'):
                msg['params'] = []
                for value in param:
                    msg['params'].append(value)
            else:
                msg['params'] = [param]
            res.append(msg)
        return res


        

