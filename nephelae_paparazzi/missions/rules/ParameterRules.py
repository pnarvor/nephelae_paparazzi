
class ParameterRules:
    """
    ParameterRules

    Base class to abstract mission parameter checking.

    Attribute
    ---------
    parameterName : str
        Name of parameter to be checked. Mostly for raising traceable exceptions.


    Methods
    -------
    check(parameter) -> boolean : raise ValueError
        raise a ValueError exception if parameter deemed inappropriate.
        Returns either the same parameter value or a corrected one in case
        of predefined behavior (like a default value).
        Default behavior is returning checked value (no check)
    """

    def __init__(self, parameterName=''):
        self.parameterName = parameterName


    def __str__(self):
        return "Rules for parameter " + self.parameterName + " : none."


    def check(self, parameter):
        return parameter



