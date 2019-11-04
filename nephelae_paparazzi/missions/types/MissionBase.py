

class MissionBase:
    """
    MissionBase

    Base mission type for all mission instances.
    Holds all common attributes such as aircraft id, duration, index...

    class Attributes
    ----------------
    parameterNames : list(str, ...)
        List of parameters names for a mission specific parameters.

    updatableNames : list(str, ...)
        List of parameters names which can be updated. Can be a subset of
        parameterNames or include other parameters.


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
     
    parameterNames = []
    updatableNames = []

    def __init__(self, missionId, aircraftId, duration):
        
        self.missionType = None
        self.missionId   = int(missionId)
        self.aircraftId  = int(aircraftId)
        self.duration    = float(duration)
        self.parameters  = {}


    def __str__(self):
        prefix = "\n  "
        maxWidth = max([len(w) for w in
                       ["aircraftId"] + list(self.parameters.keys())])
        res = "Mission " + str(self.missionType) +\
              prefix + "missionId".ljust(maxWidth)  + " : " + str(self.missionId) +\
              prefix + "aircraftId".ljust(maxWidth) + " : " + str(self.aircraftId) +\
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
        elif key == "duration":
            return self.duration
        else:
            return self.parameters[key]




        

