from nephelae_paparazzi.missions.builders import build_mission_manager, build_mission_wind_updater

from .MesonhProbe import build_mesonh_probe
from .CloudCenterTracker import build_cloud_center_tracker
from .MeteoStick  import build_meteo_stick
from .CloudSensor import build_cloud_sensor
from .Energy import build_energy

# Definition of plugin factory functions. First parameter must be an aircraft
# on which to apply a plugin
pluginFactories = {
    'Missions': build_mission_manager,
    'MesonhProbe': build_mesonh_probe,
    'CloudCenterTracker': build_cloud_center_tracker,
    'MissionWindUpdater': build_mission_wind_updater,
    'MeteoStick': build_meteo_stick,
    'CloudSensor': build_cloud_sensor,
    'Energy': build_energy
}


def load_plugins(aircraft, pluginsDesc):
    """
    Load plugins for the specified aircraft. pluginsDesc is the output of a
    parsed yaml configuration file.
    
    pluginDesc is expected to be a list. pluginsDesc elements are expected to
    be one-valued dictionaries. Keys are plugin names and values are
    dictionaries with keywords arguments for plugin factory functions.

    aircraft is an instance of nephelae_paparazzi.Aircraft.
    """

    if not isinstance(pluginsDesc, list):
        raise ValueError("The list of plugins for an aircraft  should " +
                         "be of a list type. Did you forget a '-' in front " +
                         "of all plugin names in your yaml file ?" )

    for plugin in pluginsDesc:

        if isinstance(plugin, str):
            pluginFactories[plugin](aircraft)
            continue

        if len(plugin) != 1:
            raise ValueError("Yaml format error in plugin description")

        # This takes a single key from a dictionary.
        pluginName = next(iter(plugin))
        
        # Calling a factory function
        pluginFactories[pluginName](aircraft, **plugin[pluginName])
