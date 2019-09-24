from .Messages import Message
from .Messages import UavMessage

class ApStatus(UavMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(ApStatus(msg)),
            '(^ground AP_STATUS ' + str(uavId) +
            ' .* .* .* .* .* .* \d+ .*$)'
        )

    def __init__(self, msg):
        self.type = "AP_STATUS"
        super().__init__(msg)

    def parse_data(self, words):
        self.uavId = words[0]
        self.add_field('ap_mode',           words[1])
        self.add_field('lat_mode',          words[2])
        self.add_field('horiz_mode',        words[3])
        self.add_field('gaz_mode',          words[4])
        self.add_field('gps_mode',          words[5])
        self.add_field('kill_mode',         words[6])
        self.add_field('flight_time',   int(words[7]))
        self.add_field('state_filter_mode', words[8])



