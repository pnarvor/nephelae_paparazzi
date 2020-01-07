import threading

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

    def __initplugin__(self, mapInterface, spaceX=1000, spaceY=1000):
        self.spaceX = spaceX
        self.spaceY = spaceY
        self.mapInterface = mapInterface
        self.followedCenter = None
        self.runTracking = False
        self.windMap = None

    def stop(self):
        self.runTracking = False

    def start(self):
        self.runTracking = True
        cloudCenterTracker_thread = threading.Thread(
                target=self.cloud_center_tracker_maj);
        cloudCenterTracker_thread.start()

    def cloud_center_tracker_maj(self):
        while self.runTracking:
            if not self.followedCenter is None:
                wind = self.windMap.get_wind()
                print(wind)

def build_cloud_center_tracker(aircraft, mapInterface, spaceX=1000,
        spaceY=1000):

    aircraft.load_plugin(CloudCenterTracker, mapInterface, spaceX, spaceY)
