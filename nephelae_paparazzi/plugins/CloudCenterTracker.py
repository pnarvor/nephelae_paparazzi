import threading
import time

class CloudCenterTracker:

    def __pluginmethods__():
        return [{'name'         : 'stop',
                 'method'       : CloudCenterTracker.stop,
                 'conflictMode' : 'prepend'},
                {'name'         : 'start',
                 'method'       : CloudCenterTracker.start,
                 'conflictMode' : 'append'},
                {'name'         : 'cloud_center_tracker_maj',
                 'method'       : CloudCenterTracker.cloud_center_tracker_maj,
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
                target=self.cloud_center_tracker_maj)

    def stop(self):
        self.runTracking = False
        self.cloudCenterTracker_thread.join()

    def start(self):
        self.runTracking = True
        self.cloudCenterTracker_thread.start()

    def cloud_center_tracker_maj(self):
        while self.runTracking:
            if not self.followedCenter is None:
                wind = self.windMap.get_wind()
                self.followedCenter = self.followedCenter + wind
                map0 = self.mapWhereCenterIs[self.status.position.t,
                        (self.followedCenter-self.spaceX/2):(self.followedCenter
                            +self.spaceX/2),
                        (self.followedCenter-self.spaceY/2):(self.followedCenter
                            +self.spaceY/2),
                        self.status.position.z]
            else:
                time.sleep(1)


def build_cloud_center_tracker(aircraft, mapWhereCenterIs, spaceX=1000,
        spaceY=1000):
    aircraft.load_plugin(CloudCenterTracker, mapWhereCenterIs, spaceX, spaceY)
