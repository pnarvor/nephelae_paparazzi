import pickle
import threading

from .MissionFactory import MissionFactory
from .types import missionTypes
from ..common import messageInterface
from . import InsertMode

class MissionManager:

    """
    MissionManager

    This plugin is intended to handle all custom missions for a single
    Paparazzi aircraft. Only one MissionManager is allowed for each aircraft.

    Attributes
    ----------
    missionFactories : dict({str:MissionFactory, ...})
        Factory classes to be used for instanciating missions.
        Keys are mission names, values are instances of MissionFactory.
        Will be loaded from configuration files in the future.

    pendingMissions : list(MissionType, ...)
        Missions waiting to be validated before being send to the aircraft.


    Methods
    -------
    """

    def __pluginmethods__():
        return [{'name'         : 'mission_types',
                 'method'       : MissionManager.mission_types,
                 'conflictMode' : 'error'},
                {'name'         : 'mission_parameters',
                 'method'       : MissionManager.mission_parameters,
                 'conflictMode' : 'error'},
                {'name'         : 'mission_updatables',
                 'method'       : MissionManager.mission_updatables,
                 'conflictMode' : 'error'},
                {'name'         : 'create_mission',
                 'method'       : MissionManager.create_mission,
                 'conflictMode' : 'error'},
                {'name'         : 'execute_mission',
                 'method'       : MissionManager.execute_mission,
                 'conflictMode' : 'error'}
               ]
    
    def __initplugin__(self, factories=None, inputBackupFile = None,
                       outputBackupFile = None):
        """
        Parameters
        ----------
        aircraftId : str
            The id of the aircraft this MissionManager is intended for.
            A ValueError will be raised if the id already exists in 
            MissionManager.instances.keys()

        factories : dict({str:MissionFactory, ...})
            factories used to build mission instances. This parameter is
            ignored if configFile is set.

        inputBackupFile : str
            Path to file from which to read previously created missions.
            (Used in case of a warm start configuration). Ignored if is None.

        outputBackupFile : str
            Path to file to which write created missions. To be used later
            for a warm start (usually the same as inputBackupFile.
            Ignored if is None.
        """

        self.missionFactories = factories
        self.missions         = {}
        self.lastMissionId    = 0
        self.pendingMissions  = []
        self.currentMission   = None
        self.lock             = threading.Lock()
        
        self.inputBackupFile  = inputBackupFile
        self.outputBackupFile = outputBackupFile
        if self.inputBackupFile is not None:
            self.load_mission_backup_file()


    def mission_types(self):
        return self.missionFactories.keys()


    def mission_parameters(self, missionName):
        return self.missionFactories[missionName].parameter_rules_summary()


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

        with self.lock:
            # Creating new mission instance
            mission = self.missionFactories[missionType].build(
                self.new_mission_id(), self.id, duration, **missionParameters))
            
            # Saving it to backup file for warm start
            if self.outputBackupFile is not None:
                with open(self.outputBackupFile, "ab") as f:
                    pickle.dump({mission.missionId : mission.to_dict()}, f)
            
            # Keeping a copy in self.missions and registering it for validation
            self.missions[mission.missionId] = mission
            self.pendingMissions.append(mission.missionId)
            
            # At this point everything went well, keeping last generated id
            self.lastMissionId = mission.missionId


    def new_mission_id(self):
        """
        Returns either a new id or an error if impossible.
        (TODO: implementation to be completed)
        """
        newMissionId = self.lastMissionId + 1
        if newMissionId in self.missions.keys():
            # This should never happen but TODO strengthen it just in case
            raise RuntimeError("Id of newly created mission already exists.")
        return newMissionId


    def load_mission_backup_file(self):
        """To be implemented"""

        def reload_missions(unpickledMissions):
            """
            Convenience function for converting unpickled mission into mission
            instances.
            """
            for missionId, params in unpickledMissions.items():
                if self.id != params['aircraftId']:
                    raise ValueError("Error decoding mission backup file. " +
                        "The aircraft ids do not match (got " +
                        str(params['aircraftId']) + " but current aircraft is " +
                        str(self.id) + "). Did you try to load the right file ?")
                if missionId != params['missionId']:
                    raise ValueError("Error decoding mission backup file. " +
                                     "Mission ids do not match.")
                self.missions[missionId] = \
                    self.missionFactories[params['type'].build(
                        missionId, self.id, params['duration'], **params['params']))

        # This function starts here.
        if self.inputBackupFile is None:
            return

        with self.lock:
            with open(self.inputBackupFile, 'rb') as f:
                while True:
                    # loop will exit on a EOFError, no better way with pickle
                    try:
                        # pickle read file chunks after chunks, read chunks
                        # corresponding to written chunks.
                        # (N pickle.dump = N pickle.load).
                        reload_missions(pickle.load(f))
                    except EOFError:
                        # loop exit here
                        pass
            # New last id id the biggest one from the load missions
            self.lastMissionId = max(self.missions.keys())


    def execute_mission(self):
        """Execute last mission in self.pendingMission
            To be removed when a real management is implemented"""
        self.currentMission  = self.pendingMissions[-1]
        self.pendingMissions = []
        messageInterface.send(
            self.currentMission.build_message(InsertMode.ReplaceAll))
