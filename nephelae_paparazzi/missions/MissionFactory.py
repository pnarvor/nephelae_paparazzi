from nephelae.types import Bounds

# This statement import all mission types in mission.types
# and also the missionTypes dictionary which can be used to instanciate
# any of these classes
from .types import *

class MissionFactory:

    """
    MissionFactory

    Factory class for mission instances. Mostly manage parameter Bounds.

    """

    def __init__(self, missionType, parameterBounds=None):
        """
        Parameters
        ----------

        missionType : str
            Identifier of the mission type which will be instanciated when
            calling build.
        
        parameters : dict(str, Bounds)
            keys   : Parameters for this particular mission type.
                     Not including parameters common to all mission types.
            values : Allowed bounds for this particular parameter. The factory
                     will raise an exception if these bounds are not respected
                     when building a mission.
                     Can be None or Bounds(None, None) to ignore some checks.
        """

        # All mission parameter must have bounds even if None
        # This block add missing parameters bounds and
        # set them to None
        if parameterBounds is None:
            parameterBounds = {}
        for paramName in missionTypes[missionType].parameterNames:
            if paramName not in parameterBounds.keys():
                parameterBounds[paramName] = None

        self.missionType     = missionType
        self.parameterBounds = parameterBounds


    def build(self, **missionParameters):
        """
        This is the main function to build an instance of a mission.
        This will check parameters according to bounds given in
        self.parameterBounds.
        
        After this step, the Mission instance should NOT be modified.
        """

        pass

