from .ParameterRules import ParameterRules

class AllowedValues(ParameterRules):

    """
    AllowedValues

    Raise exception if parameter not in set of default values.

    Attribute
    ---------
    allowedValues : list(AnyType, ...)
        List of allowed values for parameter.

    Methods
    -------
    check(AnyType) -> AnyType:
        Returns parameter if inside self.allowedValue, overwise raise ValueError.
    """
    def __init__(self, allowedValues=[], parameterName=''):
        super().__init__(parameterName=parameterName)
        self.allowedValues = allowedValues


    def description(self):
        return "Allowed values : " + str(self.allowedValues)


    def check(self, parameterValue):
        if parameterValue in self.allowedValues:
            return parameterValue
        else:
            raise ValueError("Forbidden parameter value : "+\
                             str(parameterValue)+". Allowed values are : "+\
                             str(self.allowedValues))


    def summary(self):
        return {'allowed_values':self.allowedValues}
