# from .SimpleBounds import SimpleBounds, AllowedValues


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
        Default behavior is returning parameter value (no check)


    summary() -> dict("str": AnyType, ...) :
        Provides a standard dictionary representing the set of rules.
        Example of result for a SimpleBounds([-1,1]) and DefaultValue(0):
            {'bounds':{'min':-1, 'max':1}, 'default': 0}
    """

    # def check_rules_consistency(rules):
    #     """
    #     Checks if rules do not contain both a SimpleBounds and a
    #     AllowedValues rule.

    #     Will raise a RuntimeError if it is the case.
    #     """

    #     if (any([isinstance(rule, SimpleBounds)  for rule in rules]) and 
    #         any([isinstance(rule, AllowedValues) for rule in rules])):
    #         # We have both a SimpleBounds rule and a AllowedValues rule in the set
    #         # This is not authorized.
    #         raise RuntimeError("It is not authorized to have both a "+\
    #                            "SimpleBounds and a AllowedValues rules in a "+\
    #                            "set of rules")


    def __init__(self, rules=[], parameterName=''):
        
        # Checking if there is no big issue with rules.
        # It will raise a RuntimeError if any issue.
        # ParameterRules.check_rules_consistency(rules)

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


    def summary(self):
        res = {}
        for rule in self.rules:
            res.update(rule.summary())
        return res



