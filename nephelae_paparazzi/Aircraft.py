import os
import threading
import utm
import time
import warnings

from copy import deepcopy

from nephelae.types import MultiObserverSubject, Pluginable, Position
from nephelae.types import NavigationRef

from .common           import messageInterface
from .plugins.loaders  import load_plugins

from .AircraftStatus import AircraftStatus


class Aircraft(MultiObserverSubject, Pluginable):

    """
    Aircraft
    
    Base class for handling paparazzi uavs through the ivy-bus. This class is
    intended to be extend with plugins.

    Base functionalities includes status and gps update, and config request.
    """

    def __init__(self, uavId, navFrame):
        MultiObserverSubject.__init__(self, ['add_status'])

        self.id           = uavId
        self.navFrame     = navFrame
        self.PprzNavFrame = None
        self.ivyBinds     = []

        self.config               = None
        self.status               = AircraftStatus(self.id, self.navFrame)
        self.currentFlightParam   = None
        self.currentNavStatus     = None
        self.currentApStatus      = None
        self.currentBat           = None
        self.currentMissionStatus = None
        self.running              = False

        # In normal conditions the status is published on a AP_STATUS message callback
        # This attribute allow to publish the status on a FLIGHT_PARAMS message
        # callback if AP_STATUS is not published by paparazzi or a message was missed.
        self.statusNotified = True


    def start(self):
        self.running = True
        self.request_config()
        self.request_navFrame()
        self.ivyBinds.append(messageInterface.bind(self.flight_param_callback,   '(ground FLIGHT_PARAM ' + str(self.id) + ' .*)'))
        self.ivyBinds.append(messageInterface.bind(self.nav_status_callback,     '(ground NAV_STATUS '   + str(self.id) + ' .*)'))
        self.ivyBinds.append(messageInterface.bind(self.ap_status_callback,      '(ground AP_STATUS '    + str(self.id) + ' .*)'))
        self.ivyBinds.append(messageInterface.bind(self.bat_callback,            '(ground BAT '          + str(self.id) + ' .*)'))
        self.ivyBinds.append(messageInterface.bind(self.mission_status_callback, '(' + str(self.id) + ' MISSION_STATUS .*)'))


    def stop(self):
        for bindId in self.ivyBinds:
            # IvyUnBindMsg(bindId)
            messageInterface.unbind(bindId)
        self.running = False


    def bat_callback(self, msg):
        self.currentBat = msg
      

    def flight_param_callback(self, flightParam):
        self.currentFlightParam = flightParam
        self.status.set_flight_param(flightParam)

        if not self.statusNotified:
            # notifying status if not notified in ap_statu_callback
            self.add_status(self.status.copy())
        self.statusNotified = False


    def nav_status_callback(self, navStatus):
        self.currentNavStatus = navStatus
        self.status.set_nav_status(navStatus)


    def ap_status_callback(self, apStatus):
        self.currentApStatus = apStatus
        self.status.set_ap_status(apStatus)

        # Notifying status observer only in ap_status callback because the 3
        # status message are sent in close sequence and this is the last one.
        self.add_status(self.status.copy())
        self.statusNotified = True


    def mission_status_callback(self, missionStatus):
        self.currentMissionStatus = missionStatus
        self.status.set_mission_status(missionStatus)


    def config_callback(self, config):
        if self.config is not None:
            return
        self.config = config
        messageInterface.unbind(self.configBindId)
        # self.configThread.join() # this is blocking everything... why ?

        print("Got config :")
        print(" - identifier:", self.config['ac_id'])
        print(" - long name :", self.config['ac_name'])
        print(" - color     :", self.config['default_gui_color'])
        
        # Ensure color is 12bit format #ffffff
        try:
            step = int((len(self.config['default_gui_color']) - 1) / 3)
            self.config['default_gui_color'] = "#" +\
                self.config['default_gui_color'][1:3] +\
                self.config['default_gui_color'][1+step:step+3] +\
                self.config['default_gui_color'][1+2*step:2*step+3]
        except Exception as e:
            warn("Could not retrieve color code :", e)
            self.config['default_gui_color'] = "#ffffff"


    def request_config(self):
        def config_request_loop(uavObj):
            count = 1
            while uavObj.config is None and self.running:
                messageInterface.send('ground ' + str(os.getpid()) + '_' +
                    str(count) + ' CONFIG_REQ ' + str(self.id))
                count = count + 1
                time.sleep(1.0)

        # function starts here
        self.configBindId = messageInterface.bind_raw(
            lambda sender, msg: messageInterface.messageInterface.parse_pprz_msg(
                lambda sender, msg: self.config_callback(msg), msg),
            '(^' + str(os.getpid()) + '_\d+ .* CONFIG ' + str(self.id) +' .*)')

        # Starting a thread to request config until we get one
        self.configThread = threading.Thread(target=config_request_loop,
                                             args=(self,))
        self.configThread.start()

    def request_navFrame(self):
        self.navFrameBindId = messageInterface.bind(self.navFrame_callback,
                '(^' + str(self.id) + ' NAVIGATION_REF .*)')

    def navFrame_callback(self, navFrame):
        return
        messageInterface.unbind(self.navFrameBindId)
        if navFrame['utm_zone'] != self.navFrame.utm_number:
            raise ValueError('navFrame and Pprz have two different values of ' +
                    'utm_zone')
        self.PprzNavFrame = NavigationRef(position=Position(
            self.navFrame.position.t, navFrame['utm_east'],
            navFrame['utm_north'], navFrame['ground_alt']),
            utm_zone=str(navFrame['utm_zone']) + self.navFrame.utm_letter)
        print('Catched Paparazzi NavigationRef for ' + str(self.id) + ' : ')
        print(self.PprzNavFrame)
        print(self.navFrame)
        warnings.simplefilter('always')
        if abs(self.PprzNavFrame.position.x - self.navFrame.position.x) > 1:
            e = UserWarning('X values between Ground NavigationRef and Pprz' +
                    'NavigationRef have a greater difference than 1 meter')
            print("{}: {}".format(type(e).__name__, e))

        if abs(self.PprzNavFrame.position.y - self.navFrame.position.y) > 1:
            e = UserWarning('Y values between Ground NavigationRef and Pprz' +
                    'NavigationRef have a greater difference than 1 meter')
            print("{}: {}".format(type(e).__name__, e))

        if abs(self.PprzNavFrame.position.z - self.navFrame.position.z) > 1:
            e = UserWarning('Z values between Ground NavigationRef and Pprz' +
                    'NavigationRef have a greater difference than 1 meter')
            print("{}: {}".format(type(e).__name__, e))

    def flight_time(self):
        return self.currentApStatus.flight_time


    # decide to keep these or not...
    def add_status_observer(self, observer):
        self.attach_observer(observer, 'add_status')
    def remove_status_observer(self, observer):
        self.detach_observer(observer, 'add_status')




