from .Messages import Message
from .Messages import UavMessage

class Ptu(UavMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(Ptu(msg)),
            '(^'+str(uavId)+' PAYLOAD_FLOAT '+
            '\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*$)'
        )

    def __init__(self, msg):
        self.type = "PAYLOAD_FLOAT"
        super().__init__(msg)

    def parse_data(self, words):
        words = words[0].split(',')
        # to be checked !
        self.add_field('pressure',    float(words[0]))
        self.add_field('temperature', float(words[1]))
        self.add_field('humidity',    float(words[2]))
        self.add_field('ptuUnknown',  float(words[3]))
    
