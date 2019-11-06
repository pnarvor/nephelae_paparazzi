from nephelae.types import MultiObserverSubject

from . import common
from .messages import Gps, FlightParam, NavStatus, ApStatus, Bat, MissionStatus, Config



class PluginableSubject(MultiObserverSubjet):

    """
    PluginableSubject

    Intermediate class for the Aircraft type to have traits from 
    the MultiObserverSubject but also be able to manage plugins.

    (Might be more suited to a double inheritance)

    Attributes
    ----------
    __safePluginLoad : bool
        This is to force safe load of plugin regardless of the users choice.
        Safe load means load will be aborted if any method name loaded by the
        plugin superseed an attribute or a method of the base class.
    """

    def __init__(self, notificationMethods, safePluginLoad=True):
        super().__init__(notificationMethods)
        self.__safePluginLoad = safePluginLoad


    def load_plugin(self, plugin, safe=True, *args, **kwargs):
        if safe or self.__safePluginLoad:
            # Checking if method name already exists in self attributes
            for method in plugin.__pluginmethods__():
                methodName = str(method).split(' ')[1].split('.')[-1]
                if hasattr(self, methodName):
                    raise RuntimeError(
                        "Cannot load plugin "+str(plugin)+", method '"+\
                         methodName+"'is already in base object"+\
                         "Load plugin in unsafe mode to override.")
        
        # Adding methods from plugin to this object
        for method in plugin.__pluginmethods__():
            setattr(self, str(method).split(' ')[1].split('.')[-1], method,
                    lambda self, *args, **kwargs: method(self, *args, **kwargs))
        # Calling plugin init function
        plugin.__plugininit__(self, *args, **kwargs)




