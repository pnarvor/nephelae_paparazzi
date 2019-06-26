import time

from ivy.std_api import *
import logging

class Message:

    def bind(callback, regex):
        return IvyBindMsg(lambda agent, msg: callback(msg), regex)

    def __init__(self, msg=""):
        self.stamp = time.time()
        self.raw = msg
        if not hasattr(self, 'type'):
            self.type = None
        self.fields = []
        self.parse(msg)

    def add_field(self, name, value):
        self.fields.append(name)
        setattr(self, name, value)

    def __getitem__(self, field):
        return getattr(self, field)

    def parse(self, msg):
        self.parse_data(msg.split(' '))

    def parse_data(self, words):
        for index, word in enumerate(words):
            self.add_field('field_' + str(index), word)

class UavMessage(Message):

    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        res = str(self.uavId) + ' ' + str(self.type) + ' :\n'
        for field in self.fields:
            res = res + ' ' + field + ' : ' + str(self[field]) + '\n'
        return res

    def parse(self, msg):
        words = msg.split(' ')
        if self.type is not None:
            if not self.type == words[1]:
                raise Exception("Got wrong message for parsing (Expected \""
                               + str(self.type) + "\" got \"" + words[1] + "\".")
        self.uavId = words[0]
        self.parse_data(words[2:])


