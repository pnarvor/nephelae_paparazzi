from .Messages import Message
from .Messages import ResponseMessage

class Config(ResponseMessage):

    def bind(callback, requestId='\d+_\d+'):
        print('(^' + str(requestId) + ' .* CONFIG .*)')
        return Message.bind(lambda msg: callback(Config(msg)),
            '(^' + str(requestId) + ' .* CONFIG .*)')

    def __init__(self, msg):
        self.type = "CONFIG"
        super().__init__(msg)

    def parse_data(self, words):
        self.add_field('ac_id',             str(words[0]))
        self.add_field('flight_plan',       str(words[1]))
        self.add_field('airframe',          str(words[2]))
        self.add_field('radio',             str(words[3]))
        self.add_field('settings',          str(words[4]))
        self.add_field('default_gui_color', str(words[5]))
        self.add_field('ac_name',           str(words[6]))

