from .Lace import Lace

# This list allows to instanciate a particular mission type from a string
# For example :
# from nephelae_paparazzi.missions.types import missionTypes
# lace = missionTypes['Lace'](...)
# Will instanciate a nephelae_paparazzi.missions.types 

missionTypes = {'Lace' : Lace}
