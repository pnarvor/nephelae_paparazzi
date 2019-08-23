from .Messages import Message
from .Messages import ResponseMessage

class WorldEnv(ResponseMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(WorldEnv(msg)),
            '(^\d+_\d+ ' + str(uavId) + ' WORLD_ENV .*)')

    def build(requestMsg,
              wind_east=0.0, wind_north=0.0, wind_up=0.0,
              ir_contrast=266.0, time_scale=1.0, gps_availability=1):
        res = WorldEnv("")
        res.requestId = requestMsg.requestId
        res.senderId  = requestMsg.senderId
        res.stamp     = requestMsg.stamp
        res.add_field('wind_east'       , wind_east)
        res.add_field('wind_north'      , wind_north)
        res.add_field('wind_up'         , wind_up)
        res.add_field('ir_contrast'     , ir_contrast)
        res.add_field('time_scale'      , time_scale)
        res.add_field('gps_availability', gps_availability)
        return res

    def __init__(self, msg=""):
        self.type = "WORLD_ENV"
        super().__init__(msg)

    def parse_data(self, words):
        self.add_field('wind_east'       , float(words[0]))
        self.add_field('wind_north'      , float(words[1]))
        self.add_field('wind_up'         , float(words[2]))
        self.add_field('ir_contrast'     , float(words[3]))
        self.add_field('time_scale'      , float(words[4]))
        self.add_field('gps_availability',   int(words[5]))

