from ..common import messageInterface
from pprzlink.message import PprzMessage
from pprzlink import messages_xml_map


class Mission:

    """Mission

    Base class for parazzi missions.

    Hold paramater list, can start a mission by building a pprzlink message.

    A mission is always attached to a uav.
    """

    # insert mods : is a non value-defined enum in
    # paparazzi/sw/airborne/modules/mission_common.h:45
    # By default in C, value in a enum are incremented starting 0
    Append         = 0
    Prepend        = 1
    ReplaceCurrent = 2
    ReplaceAll     = 3

    def __init__(self, missionType, uav, index, duration=-1.0, insertMode=Append, **kwargs):
        self.missionType = missionType
        self.uav         = uav
        self.index       = index
        self.duration    = duration
        self.insertMode  = insertMode
        self.parameters  = kwargs


    def build_pprz_message(self):
        msg = PprzMessage('datalink', self.missionType)
        msg['ac_id']    = self.uav
        msg['index']    = self.index
        msg['duration'] = self.duration
        msg['insert']   = self.insertMode
        for key in self.parameters:
            if key not in msg.fieldvalues:
                raise ValueError(key + " is not a " + self.missionType + " parameter")
            msg[key] = self.parameters[key]
        return msg


    def execute(self):
        messageInterface.send(self.build_pprz_msg)


class MissionBuilder:

    """MissionBuilder

    Base class for creating a mission.
    Will parse data from pprzlink to fetch mission parameters and
    check parameters prior building a Mission object.

    MISSION_CUSTOM not implemented yet.

    """

    missionMessagesNames = ['MISSION_GOTO_WP',
                            'MISSION_GOTO_WP_LLA',
                            'MISSION_CIRCLE',
                            'MISSION_CIRCLE_LLA',
                            'MISSION_SEGMENT',
                            'MISSION_SEGMENT_LLA',
                            'MISSION_PATH', 
                            'MISSION_PATH_LLA']

    commonParameters = ['ac_id', 'duration', 'index', 'insert']


    def get_parameter_list(missionType):
        if missionType not in MissionBuilder.missionMessagesNames:
            raise ValueError(missionType + " is not a MISSION")
        msg = PprzMessage('datalink', missionType)
        params = []
        for field in msg.fieldnames:
            # not outputing params common to all missions
            if field not in MissionBuilder.commonParameters:
                params.append(field)
        return params




