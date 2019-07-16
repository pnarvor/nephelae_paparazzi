import nephelae_base.types as ntypes

from .Messages import Message
from .Messages import UavMessage
from . import NavigationRef

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


    def __sub__(self, other):
        if type(other) == Gps:
            return ntypes.Position(self.itow - other.itow,
                                   self.utm_east - other.utm_east,
                                   self.utm_north - other.utm_north,
                                   self.alt - other.alt)
        elif type(other) == NavigationRef:
            return ntypes.Position(self.stamp - other.stamp,
                                   self.utm_east - other.utm_east,
                                   self.utm_north - other.utm_north,
                                   self.alt - other.ground_alt)
        else:
            raise ValueError("Invalid operand type")


    def to_base_type(self):
        return ntypes.Gps(self.uavId,
                          ntypes.Position(self.stamp,
                                          self.utm_east,
                                          self.utm_north,
                                          self.alt),
                          self.mode, self.course, self.speed, self.climb,
                          self.week, self.itow, self.utm_zone, self.gps_nb_err)


