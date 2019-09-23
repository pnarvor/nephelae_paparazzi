import os
import sys
import threading
import time

from ivy.std_api import *
import logging

from .. import common

class TimeoutReached(Exception):
    pass

class TimeoutLock:

    """TimeoutLock

       Convenience wrapper around threading.Lock() and threading.Condition().
       Wait for timeout or to be notified by another thread with spurious wake
       handling.

       Usage:

       TimeoutLock lock(defaultTimeout)
       lock.wait(timeout=5.0) # Wait until timeout (returns False)
                              # or until self.unlock() call (returns True)

       def callback(sleeper):
           lock.release()     # makes lock.wait to return True immediately

    """

    def __init__(self):
        
        self.notified = False
        self.cond = threading.Condition()

    def wait(self, timeout=5.0):

        self.notified = False
        with self.cond:
            startTime = time.time()
            currentTime = startTime
            while currentTime < startTime + timeout:
                if self.notified:
                    # self.notified = True
                    break
                else:
                    self.cond.wait(timeout + startTime - currentTime)
                    currentTime = time.time()
        return self.notified

    def release(self):
        with self.cond:
            # print("lock notified")
            self.notified = True
            self.cond.notify_all()

class MessageGrabber:

    def __init__(self, messageType, bindParameter=None):

        self.messageType   = messageType
        self.res           = None
        self.error         = None
        self.lock          = TimeoutLock()
        self.callbackLock  = threading.Lock()
        self.bindId        = -1
        self.bindParameter = bindParameter
        
        # Binding before grab_one call allows for safe request handling
        # (create message grabber = ivybind, send request, and only then wait for request)
        if self.bindParameter is None:
            self.bindId = self.messageType.bind(self.callback)
        else:
            self.bindId = self.messageType.bind(self.callback, self.bindParameter)
        # print("Bind id is", self.bindId)

    def grab_one(self, timeout=5.0):
        
        # return res if already grabbed
        # print("Grabbing one", flush=True)
        if self.res is not None:
            # print("Return already")
            return self.res
        # print("Go for waiting", flush=True)
        
        if not self.lock.wait(timeout):
            # raise Exception("MessageGrabber : timeout reached with regex \"" + regex + "\"")
            # print("unbinding :", self.bindId)
            IvyUnBindMsg(self.bindId)
            raise TimeoutReached()
        if self.error is not None:
            raise Exception(self, error)
        return self.res

    def callback(self, msg):
        
        with self.callbackLock:
            try:
                # print("Callback called", msg, flush=True)
                # check in case of message queue
                if self.bindId == -1:
                    # print("Returning...", flush=True)
                    return
                # print("Not returning...", flush=True)

                self.res = msg
                # print("unbinding :", self.bindId)
                IvyUnBindMsg(self.bindId)
                self.bindId = -1
                self.lock.release()
                # print("Unlocked", flush=True)
            except Exception as e:
                print("Got exception #####################", e, flush=True)
                raise e
            # print("returning\n\n")


def grab_one(messageType, timeout=60.0, bindParameter=None):

    """get_one(messageType, regex, timeout=60.0)
       
       Wait for a paparazzi message of type messageType to be
       published on the IvyBus with respect to regex,
       then returns an instance of the message type.
       If timeout is reached, throws an exception.

       Parameters:
       messageType (type): Type of the message defined in .messages
       regex        (str): regex filter to be used on the IvyBus.
       timeout    (float): timeout in seconds. Will be ignored if negative.

       Returns:
       message (messageType): Instance of messageType

    """
    # print("Call global grab")
    grabber = MessageGrabber(messageType, bindParameter)
    return grabber.grab_one(timeout)


