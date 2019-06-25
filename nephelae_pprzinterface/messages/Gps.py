from .Messages import Message
from .Messages import UavMessage

class Gps(UavMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(Gps(msg)),
                            '(' + str(uavId) + ' GPS .*)')

    def __init__(self, msg):
        self.type = "GPS"
        super().__init__(msg)

    def parse_data(self, words):
        self.add_field('mode'      ,   int(words[0]))
        self.add_field('utm_east'  , float(words[1]) / 1.0e2)
        self.add_field('utm_north' , float(words[2]) / 1.0e2)
        self.add_field('course'    , float(words[3]) / 10.0)
        self.add_field('alt'       , float(words[4]) / 1.0e3)
        self.add_field('speed'     , float(words[5]) / 1.0e2)
        self.add_field('climb'     , float(words[6]) / 1.0e2)
        self.add_field('week'      ,   int(words[7]))
        self.add_field('itow'      , float(words[8]) / 1.0e3)
        self.add_field('utm_zone'  ,   int(words[9]))
        self.add_field('gps_nb_err',   int(words[10]))
    
