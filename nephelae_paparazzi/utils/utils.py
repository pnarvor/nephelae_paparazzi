from ..common import PprzMessage, messageInterface


def send_lwc(aircraftId, lwcValue):
    """
    Helper function to send a lwc value to an aircraft.
    Mostly for debug purposes.
    """
    msg = PprzMessage('datalink', 'PAYLOAD_COMMAND')
    msg['ac_id']   = int(aircraftId)
    msg['command'] = [min(max(int(lwcValue), 0), 255)]
    messageInterface.send(msg)




