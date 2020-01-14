from threading import Timer

from ..common import messageInterface

class MissionWindUpdater:

    """
    MissionWindUpdater
    
    This plugin is intended to update the hdrift updatable of the current
    mission of an aircraft. To be applied on the nephelae_paparazzi.Aircraft
    type.

    """

    def __pluginmethods__():
        return [{'name'         : 'start',
                 'method'       : MissionWindUpdater.start,
                 'conflictMode' : 'append'},
                {'name'         : 'stop',
                 'method'       : MissionWindUpdater.stop,
                 'conflictMode' : 'prepend'},
                {'name'         : 'update_current_mission_wind',
                 'method'       : MissionWindUpdater.update_current_mission_wind,
                 'conflictMode' : 'prepend'}
               ]

    def __initplugin__(self, windMap=None, period=10.0):
        """
        Parameters
        ----------
        windMap : MapInterface
            WindMap defining a global windMap.wind attribute to use as a wind
            estimation.

        period : float
            Period in seconds at which the update will be perfomed.
        """

        self.windMap              = windMap
        self.period               = period
        self.missionUpdateTimer   = None


    def start(self):
        self.missionUpdateTimer = Timer(self.period,
                                        self.update_current_mission_wind)
        self.missionUpdateTimer.start()
        

    def stop(self):
        
        if self.missionUpdateTimer is not None:
            self.missionUpdateTimer.cancel()
        self.missionUpdateTimer = None
        

    def update_current_mission_wind(self):
        
        if self.current_mission() is not None:
            messageInterface.send(
                self.currentMission.build_update_messages(hdrift=self.windMap.wind)[0])

        # Checking if aircraft is running and stop was not requested
        if self.running and self.missionUpdateTimer is not None:
            self.missionUpdateTimer = Timer(self.period,
                                            self.update_current_mission_wind)
            self.missionUpdateTimer.start()
        else:
            # Ensuring missionUpdateTimer is None (in case self.running is false)
            self.missionUpdateTimer = None


        
