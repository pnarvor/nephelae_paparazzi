from .ParameterRules import ParameterRules

class DefaultValue(ParameterRules):

    """
    DefaultValue

    Outputs a predifined DefaultValue if parameter is None.

    Attribute
    ---------
    defaultValue : AnyType
        Output value if checked parameter is None.

    Methods
    -------
    check(AnyType) -> AnyType:
        Returns default value if parameter is None, else forward parameter value.
    """
    def __init__(self, defaultValue=None, parameterName=''):
        super().__init__(parameterName=parameterName)
        self.defaultValue = defaultValue


    def description(self):
        return "Default value : " + str(self.defaultValue)


    def check(self, parameterValue):
        if parameterValue is None:
            return self.defaultValue
        return parameterValue


    def summary(self):
        return {'default':self.defaultValue}
