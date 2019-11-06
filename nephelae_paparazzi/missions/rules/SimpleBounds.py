from nephelae.types import Bounds

from .ParameterRules import ParameterRules

class SimpleBounds(ParameterRules):

    """
    SimpleBounds

    Implements a simple bound checking.

    Attributes
    ----------
    bounds : nephelae.type.Bounds
        Bounds to compare parameter with.

    Methods
    -------
    check(AnyType) -> AnyType: raise ValueError
        If parameter is not None, check if inside self.bounds. If not, raise
        ValueError exception, if yes, returns checked parameter.
    """
    def __init__(self, bounds=None, parameterName=''):
        """
        Parameters
        ----------
        bounds : nephelae.types.Bounds

        defaultValue : any type
        """
        super().__init__(parameterName=parameterName)
        if isinstance(bounds, Bounds) or bounds is None:
            self.bounds = bounds
        else: # Assuming a list of min and max value
            self.bounds = Bounds(bounds[0], bounds[-1])


    def description(self):
        return "Bounds : " + str(self.bounds)


    def check(self, parameterValue):
        if not self.bounds.isinside(parameterValue):
            raise ValueError("Parameter " + self.parameterName + \
                             " (" + str(parameterValue) + ") is not inside " +\
                             str(self.bounds))
        return parameterValue


    def summary(self):
        return {'bounds':{'min':self.bounds.min,
                          'max':self.bounds.max}}

