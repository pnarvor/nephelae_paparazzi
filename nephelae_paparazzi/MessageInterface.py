import os
import sys
import time

# from ivy.std_api import *

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", None)
if PPRZ_HOME is not None:
    sys.path.append(PPRZ_HOME + "/var/lib/python")
else:
    PPRZLINK_HOME = os.getenv("PAPARAZZI_PPRZLINK", None)
    if PPRZLINK_HOME is not None:
        print(os.path.join(PPRZLINK_HOME, 'lib/v2.0/python'))
        sys.path.append(os.path.join(PPRZLINK_HOME, 'lib/v2.0/python'))

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage

class MessageInterface:

    """
    MessageInterface

    This is an abstraction layer used to simplify the use of paparazzi
    message interface, especially for time measurement and casting of
    message payload data (which are all str at message reception).

    """

    def prettify_message(msg):
        """
        By default paparazzi message fields are all str type despite having all
        the informations to cast fields to numeric types. This function cast
        all fields to their numeric types. (supposed to be done by 
        PprzMessage.payload_to_binay but does not seem to be working)

        It also measure reception time.
        """
        timestamp = time.time()
        fieldValues = []
        for fieldValue, fieldType in zip(msg.fieldvalues, msg.fieldtypes):
            if "int" in fieldType:
                castType = int
            elif "float" in fieldType:
                castType = float
            elif "string" in fieldType:
                castType = str
            elif "char" in fieldType:
                castType = int
            else:
                # Could not indentify type, leave field as is
                fieldValues.append(fieldValue)

            # Checking if is a list
            if '[' in fieldType:
                fieldValues.append([castType(value) for value in fieldValue])
            else:
                fieldValues.append(castType(fieldValue))
        msg.set_values(fieldValues)
        msg.timestamp = timestamp
        return msg


    def __init__(self, ivyBusAddress=None):
        
        if ivyBusAddress is None:
            ivyBusAddress = os.getenv('IVY_BUS')
            if ivyBusAddress is None:
                ivyBusAddress == ""
        self.messageInterface = IvyMessagesInterface(ivy_bus=ivyBusAddress)


    def bind(self, callback, ivyRegex):
        return self.messageInterface.subscribe(
            lambda sender, msg: callback(MessageInterface.prettify_message(msg)),
            ivyRegex)


    def bind_raw(self, callback, ivyRegex):
        return self.messageInterface.bind_raw(callback, ivyRegex)


    def unbind(self, bindId):
        self.messageInterface.unbind(bindId)

    
    def send(self, msg):
        return self.messageInterface.send(msg)
