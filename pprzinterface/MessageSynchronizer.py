from threading import Lock

class MessageSynchronizer:

    def __init__(self):
        
        self.lock = Lock()
        self.channel1 = None
        self.channel2 = None

    def update_channel1(self, msg):
        res = None
        with self.lock:
            if self.channel2 is None:
                self.channel1 = msg
            else:
                res = [msg, self.channel2]
                self.channel1 = None
                self.channel2 = None
        return res

    def update_channel2(self, msg):
        res = None
        with self.lock:
            if self.channel1 is None:
                self.channel2 = msg
            else:
                res = [self.channel1, msg]
                self.channel1 = None
                self.channel2 = None
        return res



