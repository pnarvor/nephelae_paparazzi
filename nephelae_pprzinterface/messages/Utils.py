import threading
import time

from ivy.std_api import *
import logging

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
        print("Start wait")

        self.notified = False
        with self.cond:
            startTime = time.time()
            currentTime = startTime
            while currentTime < startTime + timeout:
                if self.notified:
                    self.notified = True
                    break
                else:
                    self.cond.wait(timeout + startTime - currentTime)
                    currentTime = time.time()
        return self.notified

    def release(self):
        print("Try release")
        with self.cond:
            self.notified = True
            self.cond.notify_all()
            print("Released")

class MessageGrabber:

    def __init__(self, messageType):

        self.messageType = messageType
        self.res         = None
        self.error       = None
        self.lock        = TimeoutLock()
        self.bindId      = -1

    def grab_one(self, regex, timeout=5.0):
        
        self.bindId = IvyBindMsg(lambda agent, msg: self.callback(msg), regex)
        if not self.lock.wait(timeout):
            raise Exception("MessageGrabber : timeout reached with regex \"" + regex + "\"")
        if self.error is not None:
            raise Exception(self, error)
        return self.res

    def callback(self, msg):
        
        print("Callback called !")
        try:
            self.res = self.messageType(msg)
        except Exception as e:
            self.error = e
        IvyUnBindMsg(self.bindId)
        self.lock.release()

def grab_one(messageType, regex, timeout=60.0):

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
    grabber = MessageGrabber(messageType)
    return grabber.grab_one(regex, timeout)
