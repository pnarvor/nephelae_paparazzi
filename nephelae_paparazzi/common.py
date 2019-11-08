import os
import sys
from ivy.std_api import *

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", None)
if PPRZ_HOME is not None:
    sys.path.append(PPRZ_HOME + "/var/lib/python")
else:
    PPRZLINK_HOME = os.getenv("PAPARAZZI_PPRZLINK", None)
    if PPRZLINK_HOME is not None:
        print(os.path.join(PPRZLINK_HOME, 'lib/v2.0/python'))
        sys.path.append(os.path.join(PPRZLINK_HOME, 'lib/v2.0/python'))

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage

messageInterface = IvyMessagesInterface()

