import threading
import matplotlib.pyplot as plt
from   matplotlib import animation
import numpy as np


class DataRtDisplay:
    """
    DataRtDisplay

    Display incoming data in realtime.
    """

    def __init__(self, dataType='WT', maxData=60, openNow=True):
        self.data     = {}
        self.dataType = dataType
        self.maxData  = maxData
        self.lock     = threading.Lock()
        if openNow:
            self.draw()

    def add_sample(self,msg):
        if msg.variableName != self.dataType:
            return
        with self.lock:
            if msg.producer not in self.data.keys():
                self.data[msg.producer] = [[0.0, 0.0]]*self.maxData
            self.data[msg.producer].append([msg.timeStamp, msg.data[0]])
            self.data[msg.producer][0:1] = []

    
    def get(self):
        res = {}
        with self.lock: 
            for key in self.data.keys():
                res[key] = np.copy(self.data[key])
        return res

    
    def draw(self):

        def init():
            pass
    
        def update(i):
            global varDisp
            data = self.get()
            self.axes.clear()
            self.axes.set_title(self.dataType)
            for key in data.keys():
                self.axes.plot(data[key][:,0], data[key][:,1], '--*', label=key)
            self.axes.legend(loc="lower left")
            self.axes.set_xlabel("Time (s)")

        self.fig, self.axes = plt.subplots(1,1)
        self.anim = animation.FuncAnimation(
            self.fig,
            update,
            init_func=init,
            interval = 1)
        plt.show(block=False)
