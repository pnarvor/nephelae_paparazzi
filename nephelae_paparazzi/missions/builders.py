from .rules          import *
from .MissionFactory import MissionFactory
from .MissionManager import MissionManager

def build_rule_set(parameterName, rulesDescription):
    """

    build_rule_set

    Builds a set of rule for a parameter. rulesDescription is a list of
    single-valued dictionaries. (The list is important to conserve the rules
    order. A ValueError will be raised if rulesDescription is not a list).
    Each dictionary contains a single element representing a single rule. The
    key is the type of rule (as in nephelae_paparazzi.missions.rules) and the
    value is the list of positional parameters to be passed to the rule
    constructor.
    """
    if not isinstance(rulesDescription, list):
        raise ValueError("The list of rules for a mission parameter should " +
                         "be of a list type. Did you forget a '-' in front " +
                         "of all parameter rules in your yaml file ?" )
    
    ruleSet = []
    for rule in rulesDescription:
        if len(rule) != 1:
            raise ValueError("Yaml format error in rule definition.")

        # This takes a single key from a dictionary. key now contains a string
        # equal to the python type of rule to be instanciated. it can be
        # instanciated with eval (dangerous, fix this). Positional arguments
        # for instanciation are given in *rule[key].
        key = next(iter(rule))
        ruleSet.append(eval(key)(*(rule[key] + [parameterName])))

    return ParameterRules(ruleSet, parameterName)


def build_mission_factory(missionType, parameterRules, updateRules={}):

    """
    build_factory

    Creates a MissionFactory object from a dictionary of parameters.

    Each element in the dictionary represent a mission parameter with its
    associated rules (default argument, bounds...). The key is the parameter
    name and the value is a list of rules. 
    """

    parameters = {}
    for key in parameterRules:
        parameters[key] = build_rule_set(key, parameterRules[key])

    updatables = {}
    for key in updateRules:
        updatables[key] = build_rule_set(key, updateRules[key])

    return MissionFactory(missionType, parameters, updatables)







