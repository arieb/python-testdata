import math
import random
from ..base import Factory 
from ..errors import InvalidTotalPrecentage
from .generic import Constant

class StatisticalPercentageFactory(Factory):
    """
    Returns a different value a precentage of a time.
    :param factories: a list of 2 item tuples. each tuple contains The Factory that its result should be returned as the first item,
                                            and the chance of that value returning (in precents) as the second.
    Note:
    The sum of all precentages should be 100.
    Examples:
    >>> import testdata
    >>> f = [i for i in StatisticalPercentageFactory([(testdata.Constant('foo'), 50), (testdata.Constant('bar'), 50)]).generate(4)]
    >>> f.count('foo')
    2
    >>> f.count('bar')
    2
    >>> f = [i for i in StatisticalPercentageFactory([(testdata.Constant('foo'), 50), (testdata.Constant('bar'), 20)]).generate(4)]
    Traceback (most recent call last):
    InvalidTotalPrecentage: Need a total of a 100 precent. got 70 instead
    """
    def __init__(self, factories):
        super(StatisticalPercentageFactory, self).__init__()
        self._factories = []
        total_precentage = 0
        for factory, precent in factories:
            total_precentage += precent
            self._factories.append([factory, precent])
        if total_precentage != 100:
            raise InvalidTotalPrecentage("Need a total of a 100 precent. got {} instead".format(total_precentage))

    def set_element_amount(self, element_amount):
        super(StatisticalPercentageFactory, self).set_element_amount(element_amount)
        for i in self._factories:
            i[1] = int(math.ceil(element_amount * (i[1] / 100.0)))
            i[0].set_element_amount(i[1])

    def __call__(self):
        selected_factory = random.choice(self._factories)
        value = selected_factory[0]()
        selected_factory[1] -= 1
        if selected_factory[1] == 0:
            self._factories.remove(selected_factory)
        return value
        

class StatisticalValuesFactory(StatisticalPercentageFactory):
    """
    Returns a different value a precentage of a time.
    :param values: a list of 2 item tuples. each tuple contains the value that should be returned as the first item,
                                            and the chance of that value returning (in precents) as the second.
    Note:
    The sum of all precentages should be 100.
    Examples:
    >>> f = [i for i in StatisticalValuesFactory([('foo', 50), ('bar', 50)]).generate(4)]
    >>> f.count('foo')
    2
    >>> f.count('bar')
    2
    """
    def __init__(self, values):
        factories = [[Constant(value), precent] for value, precent in values]
        super(StatisticalValuesFactory, self).__init__(factories)
