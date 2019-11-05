
# Must be declared before other imports
class InsertMode:
    Append         = 0
    Prepend        = 1
    ReplaceCurrent = 2
    ReplaceAll     = 3

from . import types
from . import rules
from .MissionFactory import MissionFactory
from .MissionManager import MissionManager

# DEPRECATED TO BE DELETED
from .Mission import MissionBuilder

