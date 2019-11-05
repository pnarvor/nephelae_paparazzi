from nephelae.types import Bounds

# This statement import all mission types in mission.types
# and also the missionTypes dictionary which can be used to instanciate
# any of these classes
from .types import *

from .rules import ParameterRules

class MissionFactory:

    """
    MissionFactory

    Factory class for mission instances. Mostly manage parameter
    rules (Bounds, default values...).

    """

    def __init__(self, missionType, parameterRules=None):
        """
        Parameters
        ----------

        missionType : str
            Identifier of the mission type which will be instanciated when
            calling build.
        
        parametersRules : dict(str:ParameterRules, ...)
            keys : str
                Parameter names for this particular mission type.
                Not including parameters common to all mission types.
            values : ParameterRules
                Rules for a parameter (allowed bounds, default value...)
                # Allowed bounds for this particular parameter. The factory
                # will raise an exception if these bounds are not respected
                # when building a mission.
                # Can be None or Bounds(None, None) to ignore some checks.
        """

        # All mission parameter must have rules objects.
        # This block add missing ParameterRules (all permissive)
        if parameterRules is None:
            parameterRules = {}
        for paramName in missionTypes[missionType].parameterNames:
            if paramName not in parameterRules.keys():
                parameterRules[paramName] = ParameterRules(paramName)
            elif parameterRules[paramName] is None:
                parameterRules[paramName] = ParameterRules(paramName)

        self.missionType    = missionType
        self.parameterRules = parameterRules


    def build(self, missionId, aircraftId, duration, **missionParameters):
        """
        This is the main function to build an instance of a mission.
        This will check parameters according to bounds given in
        self.parameterBounds.
        
        After this step, the Mission instance should NOT be modified.
        """
        checkedParams = {}
        for key in self.parameterRules.keys():
            try:
                checkedParams[key] = self.parameterRules[key].check(missionParameters[key])
            except KeyError as e:
                raise KeyError("Missing parameter when building mission : " +\
                               key + ". Original exception feedback : " + str(e))
        # Instanciating a mission from the global missionTypes list
        # Keywords argument parameters are in a dictionary which can
        # be expanded with ** on function call.
        return missionTypes[self.missionType](missionId, aircraftId,
                                              duration, **checkedParams)


    def parameter_rules_summary(self):
        res = {}
        for key in self.parameterRules.keys():
            res[key] = self.parameterRules[key].summary()
        return res

