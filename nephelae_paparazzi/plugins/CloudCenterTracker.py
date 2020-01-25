import threading
import time

import numpy as np
from scipy.spatial import distance

from nephelae.database import CloudData
from ..common import messageInterface, PprzMessage

class CloudCenterTracker:

    def __pluginmethods__():
        return [{'name'         : 'stop',
                 'method'       : CloudCenterTracker.stop,
                 'conflictMode' : 'prepend'},
                {'name'         : 'start',
                 'method'       : CloudCenterTracker.start,
                 'conflictMode' : 'append'},
                {'name'         : 'remove_point_observer',
                 'method'       : CloudCenterTracker.remove_point_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'add_point_observer',
                 'method'       : CloudCenterTracker.add_point_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'cloud_center_to_track_setter',
                 'method'       : CloudCenterTracker
                 .cloud_center_to_track_setter,
                 'conflictMode' : 'error'},
                {'name'         : 'add_debug_tracker_observer',
                 'method'       : CloudCenterTracker.add_debug_tracker_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'remove_debug_tracker_observer',
                 'method'       : CloudCenterTracker.remove_debug_tracker_observer,
                 'conflictMode' : 'abort'},
                {'name'         : 'is_choosing_nearest_cloud_center',
                 'method'       :
                 CloudCenterTracker.is_choosing_nearest_cloud_center,
                 'conflictMode' : 'abort'},
                {'name'         : 'set_choose_nearest_cloud_center',
                 'method'       :
                 CloudCenterTracker.set_choose_nearest_cloud_center,
                 'conflictMode' : 'abort'},
                {'name'         : 'set_computing_center',
                 'method'       : CloudCenterTracker.set_computing_center,
                 'conflictMode' : 'abort'},
                {'name'         : 'cloud_center_tracker_update',
                 'method'       : CloudCenterTracker.cloud_center_tracker_update,
                 'conflictMode' : 'error'}]

    def __initplugin__(self, mapWhereCenterIs, spaceX=1000, spaceY=1000):
        self.spaceX = spaceX
        self.spaceY = spaceY
        self.mapWhereCenterIs = mapWhereCenterIs
        self.processTrackingCenterLock = threading.Lock()
        self.followedCenter = None
        self.oldTime = None
        self.runTracking = False
        self.isComputingCenter = False
        self.windMap = None
        self.chooseNearestCloudCenter = True
        self.add_notification_method('new_point')
        self.add_notification_method('tracker_debug')
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
            if self.isComputingCenter:
                with self.processTrackingCenterLock:
                    altitude = self.status.position.z
                    simTime = self.status.position.t
                    wind = self.windMap.get_wind()
                    estimatedCenter = self.followedCenter + wind*(
                            simTime - self.oldTime)
                    map0 = self.mapWhereCenterIs[simTime,
                            (estimatedCenter[0]-self.spaceX/2):
                            (estimatedCenter[0]+self.spaceX/2),
                            (estimatedCenter[1]-self.spaceY/2):
                            (estimatedCenter[1]+self.spaceY/2),
                            altitude]
                    list_cloudData = CloudData.from_scaledArray(map0,
                        threshold=self.mapWhereCenterIs.threshold)
                    oldCenter = self.followedCenter
                    if self.chooseNearestCloudCenter and list_cloudData:
                        self.followedCenter = list_cloudData[np.argmin([
                                    distance.euclidean(
                                        estimatedCenter,
                                        x.get_com()
                                    )
                            for x in list_cloudData])].get_com()
                    else:
                        self.followedCenter = estimatedCenter
                    infosToShare = {'x': self.followedCenter[0],
                            'y': self.followedCenter[1], 't': simTime, 'z':
                            altitude, 'label': "Tracked point by " + self.id, 'id':
                            self.id}
                    self.new_point(infosToShare)
                    # ---------------------- DEBUG ----------------------------
                    infosToShare['x_old'] = oldCenter[0]
                    infosToShare['y_old'] = oldCenter[1]
                    infosToShare['t_old'] = self.oldTime
                    infosToShare['map'] = self.mapWhereCenterIs
                    infosToShare['scaledArray'] = map0
                    infosToShare['space_X'] = self.spaceX
                    infosToShare['space_Y'] = self.spaceY
                    infosToShare['producer'] = self.id
                    infosToShare['centers'] = [data.get_com() for data in
                            list_cloudData]
                    infosToShare['stop'] = False
                    self.tracker_debug(infosToShare)
                    # ---------------------- END DEBUG ------------------------
                    self.oldTime = simTime
                    mission = self.current_mission()
                    if (mission is not None and 'center' in
                            mission.updatableNames):
                        messageInterface.send(mission.build_update_messages(
                                    center=[infosToShare['x'], infosToShare['y'],
                                        infosToShare['z']])[0])
            time.sleep(1)

    def cloud_center_to_track_setter(self, point, time):
        with self.processTrackingCenterLock:
            self.followedCenter = point
            self.oldTime = time

    def add_point_observer(self, observer):
        self.attach_observer(observer, 'new_point')

    def remove_point_observer(self, observer):
        self.detach_observer(observer, 'new_point')

    def add_debug_tracker_observer(self, observer):
        self.attach_observer(observer, 'tracker_debug')

    def remove_debug_tracker_observer(self, observer):
        self.detach_observer(observer, 'tracker_debug')

    def set_choose_nearest_cloud_center(self, value):
        self.chooseNearestCloudCenter = value
    
    def is_choosing_nearest_cloud_center(self):
        return self.chooseNearestCloudCenter

    def set_computing_center(self, value_computing):
        with self.processTrackingCenterLock:
            self.isComputingCenter = value_computing
            if not value_computing:
                self.tracker_debug({'stop': True})


def build_cloud_center_tracker(aircraft, mapWhereCenterIs, spaceX=1000,
        spaceY=1000):
    aircraft.load_plugin(CloudCenterTracker, mapWhereCenterIs, spaceX, spaceY)
