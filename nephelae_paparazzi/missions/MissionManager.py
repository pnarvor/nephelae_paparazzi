from .MissionFactory import MissionFactory
from .types import missionTypes

class MissionManager:

    """
    MissionManager

    This class is intended to handle all custom missions for a single
    Paparazzi aircraft. Only one MissionManager is allowed for each aircraft.

    class Attributes
    ----------------
    instances : list(str,...)
        Constains the list of instances of all MissionManagers to prevent
        the instanciation of two MissionManager for a single aircraft.

    Attributes
    ----------
    aircraftId : str
        The id of the aircraft this MissionManager is intended for.
        An exception will be raised if the id already exists in 
        MissionManager.instances.keys()

    missionFactories : dict({str:MissionFactory, ...})
        Factory classes to be used for instanciating missions.
        Keys are mission names, values are instances of MissionFactory.
        Will be loaded from configuration files in the future.


    Methods
    -------
    """
    
    instances = {}
    def __init__(self, aircraftId, configFile=None):
        """
        aircraftId : str
            The id of the aircraft this MissionManager is intended for.
            A ValueError will be raised if the id already exists in 
            MissionManager.instances.keys()

        configFile : NOT IMPLEMENTED YET
            Path to configuration file or yaml parsed data which holds the
            information for building MissionFactory instances.

            Not implemented : For now, hard coded factories are used.
        """
        if aircraftId in MissionManager.instances.keys():
            raise ValueError("A instance of MissionManager for the aircraft "+
                             str(aircraftId) + " already exists. Aborting.")
        else:
            MissionManager.instances[aircraftId] = self

        self.aircraftId = aircraftId
        self.missionFactories = {}


    def mission_types(self):
        return self.missionFactories.keys()


    def mission_parameters(self, missionName):
        return missionTypes[missionName].parameterNames


    def mission_parameters(self, missionName):
        return missionTypes[missionName].updatableNames
