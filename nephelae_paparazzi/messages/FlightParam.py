from .Messages import Message
from .Messages import UavMessage

class FlightParam(UavMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(FlightParam(msg)),
            '(^ground FLIGHT_PARAM ' + str(uavId) +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' [\-]?\d+[\.]?\d*' +
            ' \d+' +
            ' [\-]?\d+[\.]?\d*' +
            '$)'
        )

    def __init__(self, msg):
        self.type = "FLIGHT_PARAM"
        super().__init__(msg)

    def parse_data(self, words):
        self.uavId = words[0]
        self.add_field('roll',      float(words[1]))
        self.add_field('pitch',     float(words[2]))
        self.add_field('heading',   float(words[3]))
        self.add_field('lat',       float(words[4]))
        self.add_field('long',      float(words[5]))
        self.add_field('speed',     float(words[6]))
        self.add_field('course',    float(words[7]))
        self.add_field('alt',       float(words[8]))
        self.add_field('climb',     float(words[9]))
        self.add_field('agl',       float(words[10]))
        self.add_field('unix_time', float(words[11]))
        self.add_field('itow',        int(words[12]))
        self.add_field('airspeed',  float(words[13]))



