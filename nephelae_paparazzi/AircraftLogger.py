

class AircraftLogger:

    """
    AircraftLogger

    This is a simple subscriber to uav to print an aircraft status

    Intended for debug purposes.
    """

    def __init__(self, quiet=False):
        self.quiet = quiet

    def add_sample(self, msg):
        if not self.quiet:
            print(msg, end="\n\n", flush=True)

    def add_status(self, status):
        if not self.quiet:
            print(status)

    def toggle(self):
        if self.quiet:
            self.quiet = False
        else:
            self.quiet = True


    
