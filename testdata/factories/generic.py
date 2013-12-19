from copy import deepcopy
import operator

from ..errors import NoFactoriesProvided
from ..base import Factory

class Constant(Factory):
    """
    Returns the same value on each iteration.

    Example,
    >>> [i for i in Constant(1).generate(5)]
    [1, 1, 1, 1, 1]
    """
    def __init__(self, constant_value,):
        super(Constant, self).__init__()
        self._constant_value = constant_value

    def __call__(self):
        return self._constant_value

class Sum(Factory):
    """
    This factory recevies a list of factories, and on each iteration
    it returns the sum of all the given factories results.

    :param factories: An iteratable containing the factories, which results
                      we want to sum.
    :param element_amount: The amount of values that are going to be generated.
    :param sum_func: The function that will be used for summing the factories' results.

    A simple Example,
    >>> import testdata
    >>> for i in testdata.Sum([testdata.CountingFactory(10, 5), testdata.CountingFactory(1, 1)]).generate(5):
    ...     print i
    11
    17
    23
    29
    35
    """
    def __init__(self, factories=[], sum_func=operator.add):
        super(Sum, self).__init__()
        if len(factories) == 0:
            raise NoFactoriesProvided("You must pass at least one factory.")
        self._factories = deepcopy(factories)
        self._sum_func = sum_func

    def __iter__(self):
        for i, factory in enumerate(self._factories):
            self._factories[i] = iter(factory)
        return super(Sum, self).__iter__()

    def __call__(self):
        result = self._factories[0]()
        for factory in self._factories[1:]:
            result = self._sum_func(result, factory())
        return result

    def increase_index(self):
        super(Sum, self).increase_index()
        for factory in self._factories:
            factory.increase_index()
    
    def set_element_amount(self, new_element_amount):
        super(Sum, self).set_element_amount(new_element_amount)
        for factory in self._factories:
            factory.set_element_amount(new_element_amount)
