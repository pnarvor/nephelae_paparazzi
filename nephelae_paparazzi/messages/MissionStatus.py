from .Messages import Message
from .Messages import UavMessage

class MissionStatus(UavMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(MissionStatus(msg)),
            '(^' + str(uavId) + ' MISSION_STATUS '+
            '[\-]?\d+[\.]?\d* .*$)'
        )

    def __init__(self, msg):
        self.type = "MISSION_STATUS"
        super().__init__(msg)

    def parse_data(self, words):
        self.add_field('remaining_time', float(words[0]))
        self.add_field('index_list', [int(index) for index in words[1].split(',')])



