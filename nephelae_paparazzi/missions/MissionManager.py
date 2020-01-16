import os.path
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
                {'name'         : 'mission_parameter_names',
                 'method'       : MissionManager.mission_parameter_names,
                 'conflictMode' : 'error'},
                {'name'         : 'mission_parameter_tags',
                 'method'       : MissionManager.mission_parameter_tags,
                 'conflictMode' : 'error'},
                {'name'         : 'mission_parameter_rules',
                 'method'       : MissionManager.mission_parameter_rules,
                 'conflictMode' : 'error'},
                {'name'         : 'mission_updatable_names',
                 'method'       : MissionManager.mission_updatable_names,
                 'conflictMode' : 'error'},
                {'name'         : 'mission_updatable_tags',
                 'method'       : MissionManager.mission_updatable_tags,
                 'conflictMode' : 'error'},
                {'name'         : 'mission_updatable_rules',
                 'method'       : MissionManager.mission_updatable_rules,
                 'conflictMode' : 'error'},
                {'name'         : 'create_mission',
                 'method'       : MissionManager.create_mission,
                 'conflictMode' : 'error'},
                {'name'         : 'new_mission_id',
                 'method'       : MissionManager.new_mission_id,
                 'conflictMode' : 'error'},
                {'name'         : 'load_mission_backup_file',
                 'method'       : MissionManager.load_mission_backup_file,
                 'conflictMode' : 'error'},
                {'name'         : 'current_mission',
                 'method'       : MissionManager.current_mission,
                 'conflictMode' : 'error'},
                {'name'         : 'current_mission_status',
                 'method'       : MissionManager.current_mission_status,
                 'conflictMode' : 'error'},
                {'name'         : 'get_pending_missions',
                 'method'       : MissionManager.get_pending_missions,
                 'conflictMode' : 'error'},
                {'name'         : 'authorize_mission',
                 'method'       : MissionManager.authorize_mission,
                 'conflictMode' : 'error'},
                {'name'         : 'reject_mission',
                 'method'       : MissionManager.reject_mission,
                 'conflictMode' : 'error'},
                {'name'         : 'do_validate_mission',
                 'method'       : MissionManager.do_validate_mission,
                 'conflictMode' : 'error'},
                {'name'         : 'validate_all',
                 'method'       : MissionManager.validate_all,
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

        self.add_notification_method('mission_uploaded')
        self.missionFactories = factories
        self.missions         = {}
        self.lastMissionId    = 0
        self.pendingMissions  = []
        self.lock             = threading.Lock()
        
        self.inputBackupFile  = inputBackupFile
        self.outputBackupFile = outputBackupFile
        if self.inputBackupFile is not None:
            self.load_mission_backup_file()


    def mission_types(self):
        return self.missionFactories.keys()


    def mission_parameter_names(self, missionName):
        return self.missionFactories[missionName].parameter_names()


    def mission_parameter_tags(self, missionName):
        return self.missionFactories[missionName].parameter_tags()


    def mission_parameter_rules(self, missionName):
        return self.missionFactories[missionName].parameter_rules_summary()


    def mission_updatable_names(self, missionName):
        return self.missionFactories[missionName].updatable_names()


    def mission_updatable_tags(self, missionName):
        return self.missionFactories[missionName].updatable_tags()


    def mission_updatable_rules(self, missionName):
        return self.missionFactories[missionName].updatable_rules_summary()


    def create_mission(self, missionType, insertMode=InsertMode.Append, duration=-1.0, **missionParameters):
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
                self.new_mission_id(), self.id, insertMode, duration, **missionParameters)
            
            # Keeping a copy in self.missions and registering it for validation
            self.missions[mission.missionId] = mission
            self.pendingMissions.append(mission.missionId)
            
            # Saving it to backup file for warm start
            if self.outputBackupFile is not None:
                with open(self.outputBackupFile, "ab") as f:
                    pickle.dump({mission.missionId : mission.to_dict()}, f)
                    pickle.dump({'pendingMissions' : self.pendingMissions}, f)
            
            # At this point everything went well, keeping last generated id
            self.lastMissionId = mission.missionId

            # self.validate_all();


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

        def reload_missions(unpickledMissions):
            """
            Convenience function for converting unpickled mission into mission
            instances.
            """
            for missionId, params in unpickledMissions.items():
                 
                # A true file format would be nice
                if missionId == 'pendingMissions':
                    self.pendingMissions = params
                    continue

                if str(self.id) != str(params['aircraftId']):
                    raise ValueError("Error decoding mission backup file. " +
                        "The aircraft ids do not match (got " +
                        str(params['aircraftId']) + " but current aircraft is " +
                        str(self.id) + "). Did you try to load the right file ?")
                if missionId != params['missionId']:
                    raise ValueError("Error decoding mission backup file. " +
                                     "Mission ids do not match.")
                self.missions[missionId] = \
                    self.missionFactories[params['type']].build(
                        missionId, self.id, params['insertMode'], params['duration'], **params['parameters'])

        # This function starts here.
        if self.inputBackupFile is None or \
           not os.path.exists(self.inputBackupFile):
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
                        break
            # New last id id the biggest one from the load missions
            self.lastMissionId = max(self.missions.keys())


    def current_mission(self):
        """
        Return current mission of the UAV
        (First in the MISSION_STATUS list)
        """
        try:
            return self.missions[self.status.mission_task_list[0]]
        except KeyError:
            return None


    def current_mission_status(self):
        res = {'current_mission_time_left': self.status.mission_time_left,
               'missions': []} 
        try:
            for missionId in self.status.mission_task_list:
                res['missions'].append(self.missions[missionId])
            return res
        except KeyError:
            return None


    def get_pending_missions(self):
        """
        Returns mission instances waiting to be authorized.
        """
        res = [];
        for missionId in self.pendingMissions:
            res.append(self.missions[missionId])
        return res;


    def authorize_mission(self, missionId):
        """
        Effectively sends a message to the aircraft with the mission.
        """
        if self.pendingMission[0] != missionId:
            # Error, pendingMission is a fifo. Cannot authorized mission other
            # than the first one in the list.
            if missionId in self.pendingMission:
                raise ValueError("You have to validate mission in " +
                                 "the order of creation")
            else:
                raise AttributeError("Unknown mission")
        else:
            self.do_validate_mission(missionId);
    
    def do_validate_mission(self, missionId):
        """
        Sends a message to aircraft to add the mission, and removes it from
        pending mission list.

        TODO : verify that the mission was received by the aircraft before
        removing it from self.pendingMissions.
        """
        messageInterface.send(self.missions[missionId].build_message())
        
        # if missionReceived:
        self.pendingMission.pop(0);
        # else:
            # raise error ?


    def reject_mission(self, missionId):
        """
        Removes a mission from self.pendingMissions without sending it to the
        aircraft.
        """
        self.pendingMissions.remove(missionId)


    def validate_all(self):
        for mission in self.pendingMissions:
            messageInterface.send(self.missions[mission].build_message())
        self.pendingMissions = []
        self.mission_uploaded()


    def execute_mission(self):
        """Execute last mission in self.pendingMission
            To be removed when a real management is implemented"""

        self.pendingMissions = []
        messageInterface.send(self.currentMission.build_message())
