from .Lace     import Lace
from .Rosette  import Rosette
from .Spiral3D import Spiral3D
from .Trinity  import Trinity

from .RosetteLeft  import RosetteLeft
from .RosetteRight  import RosetteRight

# This list allows to instanciate a particular mission type from a string
# For example :
# from nephelae_paparazzi.missions.types import missionTypes
# lace = missionTypes['Lace'](...)
# Will instanciate a nephelae_paparazzi.missions.types 

missionTypes = {'Lace'     : Lace,
                'Rosette'  : Rosette,
                'Spiral3D' : Spiral3D,
                'Trinity'  : Trinity,
                'RosetteLeft'  : RosetteLeft,
                'RosetteRight'  : RosetteRight
               }
