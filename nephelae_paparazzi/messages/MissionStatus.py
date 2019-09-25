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
        indexes = []
        for index in words[1].split(','):
            try:
                value = int(index)
            except ValueError:
                continue
            indexes.append(value)
        self.add_field('index_list', indexes)



