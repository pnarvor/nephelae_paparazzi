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

    def __init__(self, missionType, parameterRules=None, updateRules=None):
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
                parameterRules[paramName] = ParameterRules([], paramName)
            elif parameterRules[paramName] is None:
                parameterRules[paramName] = ParameterRules([], paramName)
        for key in parameterRules.keys():
            if isinstance(parameterRules[key], list):
                parameterRules[key] = ParameterRules(parameterRules[key], key)
        
        # Same for update parameters
        if updateRules is None:
            updateRules = {}
        for paramName in missionTypes[missionType].updatableNames:
            if paramName not in updateRules.keys():
                updateRules[paramName] = ParameterRules([], paramName)
            elif updateRules[paramName] is None:
                updateRules[paramName] = ParameterRules([], paramName)
        for key in updateRules.keys():
            if isinstance(updateRules[key], list):
                updateRules[key] = ParameterRules(updateRules[key], key)

        self.missionType    = missionType
        self.parameterRules = parameterRules
        self.updatableRules = updateRules


    def __str__(self):
        res = "Parameters :\n   "
        for key in self.parameterRules.keys():
            tmp = self.parameterRules[key].description()
            res = res + tmp.replace('\n','\n   ')
        res = res[:-3] + "Update rules :\n   "
        for key in self.updatableRules.keys():
            tmp = self.updatableRules[key].description()
            res = res + tmp.replace('\n','\n   ')
        res = "MissionFactory for mission " + self.missionType + '\n   ' +\
              res.replace('\n','\n   ')
        return res


    def build(self, missionId, aircraftId, insertMode, duration,
        positionOffset=None, navFrame=None, pprzNavFrame=None,
        **missionParameters):
        """
        This is the main function to build an instance of a mission.
        This will check parameters according to bounds given in
        self.parameterBounds.
        
        After this step, the Mission instance should NOT be modified.
        """
        checkedParams = {}
        for key in self.parameterRules.keys():
            try:
                parameter = missionParameters[key]
            except KeyError as e:
                parameter = None
            checkedParams[key] = self.parameterRules[key].check(parameter)
        # Instanciating a mission from the global missionTypes list
        # Keywords argument parameters are in a dictionary which can
        # be expanded with ** on function call.
        return missionTypes[self.missionType](missionId, aircraftId,
                                              insertMode, duration,
                                              positionOffset,
                                              navFrame, pprzNavFrame,
                                              updateRules=self.updatableRules,
                                              **checkedParams)

    def parameter_names(self):
        return missionTypes[self.missionType].parameterNames


    def parameter_tags(self):
        return missionTypes[self.missionType].parameterTags


    def parameter_rules_summary(self):
        res = {}
        for key in self.parameterRules.keys():
            res[key] = self.parameterRules[key].summary()
        return res


    def updatable_names(self):
        return missionTypes[self.missionType].updatableNames


    def updatable_tags(self):
        return missionTypes[self.missionType].updatableTags


    def updatable_rules_summary(self):
        res = {}
        for key in self.updatableRules.keys():
            res[key] = self.updatableRules[key].summary()
        return res



