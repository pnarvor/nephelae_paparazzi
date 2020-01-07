class CloudCenterTracker:

    def __pluginmethods__():
        return [{'name'         : 'stop',
                 'method'       : CloudCenterTracker.stop,
                 'conflictMode' : 'prepend'},
                 'name'         : 'start',
                 'method'       : CloudCenterTracker.start,
                 'conflictMode' : 'append'];

    def __initplugin__(self):
        pass

    def stop(self):
        pass

    def start(self):
        pass
