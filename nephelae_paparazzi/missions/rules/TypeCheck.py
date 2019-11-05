from .ParameterRules import ParameterRules

class TypeCheck(ParameterRules):

    """
    TypeCheck

    Implements a type checking.

    Attribute
    ---------
    allowedTypes : tuple(any type, ...)
        A tuple of types to check. Check will be done by
        isinstance(params, self.types)

    Methods
    -------
    check(AnyType) -> AnyType: raise TypeError
        return parameter is is any of the types contained in self.types.
    """
    def __init__(self, allowedTypes=(), parameterName=''):
        super().__init__(parameterName=parameterName)
        self.allowedTypes = allowedTypes


    def description(self):
        return "Allowed types : " + str(self.allowedTypes)


    def check(self, parameterValue):
        if not isinstance(parameterValue, self.allowedTypes):
            raise TypeError("Type of parameter " + self.parameterName + \
                            " is not amongst " + str(self.allowedTypes))
        return parameterValue


    def summary(self):
        return {'allowed_types':str(self.allowedTypes)}
