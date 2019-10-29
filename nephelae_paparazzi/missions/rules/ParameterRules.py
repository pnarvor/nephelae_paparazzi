
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

    def __init__(self, rules=[], parameterName=''):
        self.parameterName = parameterName
        self.rules = rules


    def __str__(self):
        res = "Rules for parameter " + self.parameterName
        if isinstance(self, ParameterRules):
            if not self.rules:
                res = res + " : None."
            else:
                for rule in self.rules:
                    res = res + "\n  " + rule.description()
        else:
            res = res + "\n  " + self.description()

    
    def check(self, parameter):
        for rule in self.rules:
            parameter = rule.check(parameter)
        return parameter



