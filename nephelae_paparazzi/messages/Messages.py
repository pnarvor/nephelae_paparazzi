import time

from ivy.std_api import *
import logging

class Message:

    def bind(callback, regex):
        return IvyBindMsg(lambda agent, msg: callback(msg), regex)

    def unbind(ivyBindId):
        IvyUnBindMsg(ivyBindId)

    def send(self):
        IvySendMsg(self.ivy_string())

    def __init__(self, msg=""):
        self.stamp = time.time()
        self.raw = msg
        if not hasattr(self, 'type'):
            self.type = None
        self.fields = []
        if msg:
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

    def data_string(self):
        
        if not self.fields:
            return ""
        res = str(getattr(self, self.fields[0]))
        for field in self.fields[1:]:
            res = res + ' ' + str(getattr(self, field))
        return res

    def print(self):
        print(self)


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

    def ivy_string(self):
        return str(self.uavId) + ' ' + str(self.type) + ' ' + self.data_string()


class RequestMessage(Message):

    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        res = str(self.senderId)+' '+self.requestId+' '+str(self.type)+' :\n'
        for field in self.fields:
            res = res + ' ' + field + ' : ' + str(self[field]) + '\n'
        return res

    def parse(self, msg):
        words = msg.split(' ')
        if self.type is not None:
            if not self.type == words[2]:
                raise Exception("Got wrong message for parsing (Expected \""
                               + str(self.type) + "\" got \"" + words[1] + "\".")
        self.senderId  = words[0]
        self.requestId = words[1]
        self.parse_data(words[3:])

    def ivy_string(self):
        return (str(self.senderId) + ' ' + str(self.requestId) + ' ' +
                str(self.type) + ' ' + self.data_string())

    def sender_pid(self):
        return self.requestId.split('_')[0]


class ResponseMessage(Message):

    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        res = self.requestId+' '+str(self.senderId)+' '+str(self.type)+' :\n'
        for field in self.fields:
            res = res + ' ' + field + ' : ' + str(self[field]) + '\n'
        return res

    def parse(self, msg):
        words = msg.split(' ')
        if self.type is not None:
            if not self.type == words[2]:
                raise Exception("Got wrong message for parsing (Expected \""
                               + str(self.type) + "\" got \"" + words[1] + "\".")
        self.senderId  = words[1]
        self.requestId = words[0]
        self.parse_data(words[3:])

    def ivy_string(self):
        return (str(self.requestId) + ' ' + str(self.senderId) + ' ' + 
                str(self.type) + ' ' + self.data_string())


class RawDataLinkMessage(Message):

    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        res = str(self.uavId) + ' ' + str(self.type) + ' :\n'
        for field in self.fields:
            res = res + ' ' + field + ' : ' + str(self[field]) + '\n'
        return res

    def parse(self, msg):
        words = msg.split(' ')

        if words[1] != "RAW_DATALINK":
            raise Exception("Got wrong message for parsing (Expected "
                            + "\"RAW_DATALINK\" got \"" + words[1] + "\".")
        self.uavId = words[2]
        data = words[3].split(';')
        if self.type is not None:
            if not self.type == data[0]:
                raise Exception("Got wrong message for parsing (Expected \""
                               + str(self.type) + "\" got \"" + words[1] + "\".")
        self.parse_data(data[2:])


