from .Messages import Message
from .Messages import RawDataLinkMessage

class WindInfo(RawDataLinkMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(WindInfo(msg)),
            '(^dl RAW_DATALINK '+str(uavId)+' WIND_INFO;'+
            '\d+;\d+;\d+[\.]?\d*;\d+[\.]?\d*;\d+[\.]?\d*;\d+[\.]?\d*$)'
        )

    def __init__(self, msg):
        self.type = "WIND_INFO"
        super().__init__(msg)

    def parse_data(self, words):
        self.add_field('flags',      int(words[0]))
        self.add_field('east',     float(words[1]))
        self.add_field('north',    float(words[2]))
        self.add_field('up',       float(words[3]))
        self.add_field('airspeed', float(words[4]))

    
