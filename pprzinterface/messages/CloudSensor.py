from .Messages import Message
from .Messages import UavMessage

class CloudSensor(UavMessage):

    def bind(callback, uavId='.*'):
        return Message.bind(lambda msg: callback(CloudSensor(msg)),
            '(^'+str(uavId)+' PAYLOAD_FLOAT '+
            '\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*,\d+[\.]?\d*$)'
        )

    def __init__(self, msg):
        self.type = "PAYLOAD_FLOAT"
        super().__init__(msg)

    def parse_data(self, words):
        words = words[0].split(',')
        # to be checked !
        for index,word in enumerate(words):
            self.add_field('var_'+str(index), float(word))
    
