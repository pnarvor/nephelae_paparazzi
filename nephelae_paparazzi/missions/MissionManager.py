from .MissionFactory import MissionFactory
from .types import missionTypes
from ..common import messageInterface
from . import InsertMode

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

    pendingMissions : list(MissionType, ...)
        Missions waiting to be validated before being send to the aircraft.


    Methods
    -------
    """
    
    instances = {}
    def __init__(self, aircraftId, configFile=None, factories=None):
        """
        Parameters
        ----------
        aircraftId : str
            The id of the aircraft this MissionManager is intended for.
            A ValueError will be raised if the id already exists in 
            MissionManager.instances.keys()

        configFile : NOT IMPLEMENTED YET
            Path to configuration file or yaml parsed data which holds the
            information for building MissionFactory instances. If this
            parameter is set, the parameter factories is ignored.

            Not implemented : For now, hard coded factories are used.

        factories : dict({str:MissionFactory, ...})
            factories used to build mission instances. This parameter is
            ignored if configFile is set.
        """
        if aircraftId in MissionManager.instances.keys():
            raise ValueError("A instance of MissionManager for the aircraft "+
                             str(aircraftId) + " already exists. Aborting.")
        else:
            MissionManager.instances[aircraftId] = self

        self.aircraftId = aircraftId
        if configFile is not None:
            raise ValueError("Configuration files are not yet implemented !")
        else:
            self.missionFactories = factories

        self.lastMissionId   = 0
        self.pendingMissions = []


    def mission_types(self):
        return self.missionFactories.keys()


    def mission_parameters(self, missionName):
        return missionTypes[missionName].parameterNames


    def mission_updatables(self, missionName):
        return missionTypes[missionName].updatableNames


    def create_mission(self, missionType, duration=-1.0, **missionParameters):
        """
        Creates a mission instance and append it to self.pendingMissions.

        Parameters
        ----------
        missionType : str
            Mission type to be created. (Must be declared in .types.missionTypes).
        
        duration : float
            Mission duration in seconds (-1 is infinite).

        missionParameters : keyword arguments
            Parameters to be passed to the mission factory for intanciating
            this mission.
        """

        if missionType not in self.mission_types():
            raise ValueError("Cannot create a " + missionType + " for this aircraft.")

        self.pendingMissions.append(self.missionFactories[missionType].build(
            self.lastMissionId+1, self.aircraftId, duration, **missionParameters))

        self.lastMissionId = self.lastMissionId + 1

    
    def execute(self):
        """Execute last mission in self.pendingMission
            To be removed when a real management is implemented"""
        messageInterface.send(
            self.pendingMissions[-1].build_message(InsertMode.ReplaceAll))
        self.pendingMissions = []
