import threading
import time

import numpy as np
from scipy.spatial import distance

from nephelae.database import CloudData

class CloudCenterTracker:

    def __pluginmethods__():
        return [{'name'         : 'stop',
                 'method'       : CloudCenterTracker.stop,
                 'conflictMode' : 'prepend'},
                {'name'         : 'start',
                 'method'       : CloudCenterTracker.start,
                 'conflictMode' : 'append'},
                {'name'         : 'cloud_center_tracker_update',
                 'method'       : CloudCenterTracker.cloud_center_tracker_update,
                 'conflictMode' : 'error'}]

    def __initplugin__(self, mapWhereCenterIs, spaceX=1000, spaceY=1000):
        self.spaceX = spaceX
        self.spaceY = spaceY
        self.mapWhereCenterIs = mapWhereCenterIs
        self.followedCenter = None
        self.oldTime = None
        self.runTracking = False
        self.windMap = None
        self.cloudCenterTracker_thread = threading.Thread(
                target=self.cloud_center_tracker_update)

    def stop(self):
        self.runTracking = False
        self.cloudCenterTracker_thread.join()

    def start(self):
        self.runTracking = True
        self.cloudCenterTracker_thread.start()

    def cloud_center_tracker_update(self):
        while self.runTracking:
            if not self.followedCenter is None:
                altitude = self.status.position.z
                simTime = self.status.position.t
                wind = self.windMap.get_wind()
                self.followedCenter = self.followedCenter + wind*(
                        simTime - self.oldTime)
                map0 = self.mapWhereCenterIs[simTime,
                        (self.followedCenter-self.spaceX/2):(self.followedCenter
                            +self.spaceX/2),
                        (self.followedCenter-self.spaceY/2):(self.followedCenter
                            +self.spaceY/2),
                        altitude]
                self.oldTime = simTime
                list_cloudData = CloudData.from_scaledArray(map0)
                if list_cloudData:
                    self.followedCenter = list_cloudData[np.argmin([
                        distance.euclidean(self.followedCenter, x.get_com())
                        for x in list_cloudData])].get_com()
            else:
                time.sleep(1)


def build_cloud_center_tracker(aircraft, mapWhereCenterIs, spaceX=1000,
        spaceY=1000):
    aircraft.load_plugin(CloudCenterTracker, mapWhereCenterIs, spaceX, spaceY)
