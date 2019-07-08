from .Messages import Message
from .Messages import RequestMessage

class WorldEnvReq(RequestMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(WorldEnvReq(msg)),
            '(^' + str(uavId) + ' \d+_\d+ WORLD_ENV_REQ .*)')

    def __init__(self, msg):
        self.type = "WORLD_ENV_REQ"
        super().__init__(msg)

    def parse_data(self, words):
        self.add_field('lat'      , float(words[0]))
        self.add_field('long'     , float(words[1]))
        self.add_field('alt'      , float(words[2]))
        self.add_field('utm_east' , float(words[3]))
        self.add_field('utm_north', float(words[4]))
        self.add_field('up'       , float(words[5]))


