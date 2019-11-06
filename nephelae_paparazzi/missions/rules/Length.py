from .ParameterRules import ParameterRules

class Length(ParameterRules):

    """
    Length

    Check length of parameter.

    Attribute
    ---------
    length : int
        Allowed length for parameter.

    Methods
    -------
    check(AnyType) -> AnyType:
        Return parameter if len(param) == self.length. Else raise 
    """
    def __init__(self, length, parameterName=''):
        super().__init__(parameterName=parameterName)
        self.length = length


    def description(self):
        return "length : " + str(self.length)


    def check(self, parameterValue):
        if len(parameterValue) == self.length:
            return parameterValue
        else:
            raise ValueError("Parameter "+parameterValue+" should be "+\
                             str(self.length)+" length")


    def summary(self):
        return {'length':self.length}
