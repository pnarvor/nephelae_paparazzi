from .Messages import Message
from .Messages import UavMessage

class NavStatus(UavMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(NavStatus(msg)),
            '(^ground NAV_STATUS ' + str(uavId) +
            ' \d+' +
            ' \d+' +
            ' \d+' +
            ' \d+' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            '$)'
        )

    def __init__(self, msg):
        self.type = "NAV_STATUS"
        super().__init__(msg)

    def parse_data(self, words):
        self.uavId = words[0]
        self.add_field('cur_block',       int(words[1]))
        self.add_field('cur_stage',       int(words[2]))
        self.add_field('block_time',      int(words[3]))
        self.add_field('stage_time',      int(words[4]))
        self.add_field('target_lat',    float(words[5]))
        self.add_field('target_long',   float(words[6]))
        self.add_field('target_climb',  float(words[7]))
        self.add_field('target_alt',    float(words[8]))
        self.add_field('target_course', float(words[9]))
        self.add_field('dist_to_wp',    float(words[10]))



