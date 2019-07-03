from threading import Lock

class MessageSynchronizer:

    """MessageSynchronizer

    Generate synched pair of data. left and right channels are supposedly
    two asynchronous sample feed. When a channel is updated, the update 
    function returns a pair with the sample contains in each channel.
    If one of the channels does not contains a sample, then the function
    update the current channel state and returns None

    Methods:

    update_left_channel  : update current sample in left channel.
                           If right channel contains a sample, a pair of sample
                           if returned and both channels are set to None.

                           Returns : either a pair of samples or None

    update_right_channel : same as above but mirrored.

                           Returns : either a pair of samples or None

    /!\/!\/!\ This synchronizer is not currently using time stamp based
              synchronization. If the computer is under heavy load,
              or if the latency of the channels are different,
              time synchronization is not guaranteed.
    """

    def __init__(self):
        
        self.lock = Lock()
        self.leftChannel  = None
        self.rightChannel = None

    def update_left_channel(self, msg):
        res = None
        with self.lock:
            if self.rightChannel is None:
                self.leftChannel = msg
            else:
                res = [msg, self.rightChannel]
                self.leftChannel = None
                self.rightChannel = None
        return res

    def update_right_channel(self, msg):
        res = None
        with self.lock:
            if self.leftChannel is None:
                self.rightChannel = msg
            else:
                res = [self.leftChannel, msg]
                self.leftChannel = None
                self.rightChannel = None
        return res



