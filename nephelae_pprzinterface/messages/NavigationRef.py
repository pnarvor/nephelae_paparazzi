from .Messages import UavMessage

class NavigationRef(UavMessage):

    def __init__(self, msg):
        self.type = "NAVIGATION_REF"
        super().__init__(msg)

    def parse_data(self, words):
        self.add_field('utm_east'  , float(words[0]))
        self.add_field('utm_north' , float(words[1]))
        self.add_field('utm_zone'  ,   int(words[2]))
        self.add_field('ground_alt', float(words[3]))


