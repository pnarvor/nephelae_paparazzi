

class AircraftLogger:

    """
    AircraftLogger

    This is a simple subscriber to uav to print an aircraft status

    Intended for debug purposes.
    """

    def __init__(self):
        pass

    def add_sample(self, msg):
        print(msg, end="\n\n", flush=True)

    def add_gps(self, msg):
        print(msg, end="\n\n", flush=True)

    def notify_status(self, status):
        print(status)

