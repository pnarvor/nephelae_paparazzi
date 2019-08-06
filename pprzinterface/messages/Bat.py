from .Messages import Message
from .Messages import UavMessage

class Bat(UavMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(Bat(msg)),
            '(^'+str(uavId)+' BAT '+
            '\d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+$)'
        )

    def __init__(self, msg):
        self.type = "BAT"
        super().__init__(msg)

    def parse_data(self, words):

        self.add_field('throttle',           int(words[0]))
        self.add_field('voltage',        0.1*int(words[1]))
        self.add_field('amps',         0.001*int(words[2]))
        self.add_field('flight_time',        int(words[3]))
        self.add_field('kill_auto_throttle', int(words[4]))
        self.add_field('block_time',         int(words[5]))
        self.add_field('stage_time',         int(words[6]))
        self.add_field('energy',             int(words[7]))
    
