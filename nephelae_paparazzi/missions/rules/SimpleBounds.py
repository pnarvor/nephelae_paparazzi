from nephelae.types import Bounds

from .ParameterRules import ParameterRules

class SimpleBounds(ParameterRules):

    """
    SimpleBounds

    Implements a simple bound checking and a default value.

    Attributes
    ----------
    bounds : nephelae.type.Bounds
        Bounds to compare parameter with.
    
    defaultValue : ?
        Default parameter value to return if checked parameter is None.


    Methods
    -------
    check(parameter) -> boolean: raise ValueError
        If parameter is None returns self.defaultValue (if self.defaultValue
        is None, raise ValueError exception).
        If parameter is not None, check if inside self.bounds. If not, raise
        ValueError exception, if yes, returns checked parameter.
    """
    def __init__(self, parameterName='', bounds=None, defaultValue=None):
        """
        Parameters
        ----------
        bounds : nephelae.types.Bounds

        defaultValue : any type
        """
        super().__init__(parameterName)
        if isinstance(bounds, Bounds) or bounds is None:
            self.bounds = bounds
        else: # Assuming a list of min and max value
            self.bounds = Bounds(bounds[0], bounds[-1])
        self.defaultValue = defaultValue


    def __str__(self):
        return "Rules for parameter " + self.parameterName +\
               "\n  default value : " + str(self.defaultVale) +\
               "\n  bounds        : " + str(self.bounds)


    def check(self, parameterValue):
        if parameterValue is None:
            if self.defaultValue is None:
                raise ValueError("Default value not defined for " +
                                 self.parameterName)
            else:
                return self.defaultValue
        if self.bounds is None:
            return parameterValue
        if not self.bounds.isinside(parameterValue):
            raise ValueError("Parameter " + self.parameterName + \
                            " (" + str(parameterValue) + ") is not inside " +\
                            str(self.bounds))
        return parameterValue

    

