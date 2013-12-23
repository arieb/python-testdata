from copy import deepcopy
import random
import operator

from ..errors import NoFactoriesProvided
from ..base import Factory, DependentField

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

class RandomLengthListFactory(Factory):
    """
    A factory that returns on each iteration a list of of between `min` and `max` items, returned 
    from calls to the given factory.

    Example,
    >> import testdata
    >> f = RandomLengthListFactory(testdata.CountingFactory(1), 3, 8).generate(5)
    >> list(f)
    [[1, 2, 3], [4, 5, 6, 7], [8, 9, 10], [11, 12,13, 14, 15]]
    """
    def __init__(self, factory=None, min_items=0, max_items=1):
        super(RandomLengthListFactory, self).__init__()
        self._factory = factory
        self._min_items = min_items
        self._max_items = max_items

    def __iter__(self):
        self._factory = iter(self._factory)
        return super(RandomLengthListFactory, self).__iter__()

    def set_element_amount(self, element_amount):
        super(RandomLengthListFactory, self).set_element_amount(element_amount)
        self._factory.set_element_amount(element_amount * self._max_items)

    def __call__(self):
        return [self._factory.next() for i in xrange(random.randint(self._min_items, self._max_items))]

class ConditionalValueField(DependentField):
    """
    This factory returns a value depending on the value of a different field 'other_field'.
    Possible values are passed as a dict, with a key being the value of 'other_field'.

    Important!
    `possible_values` should cover all possible values of `other_field`

    For example,
    >>> import testdata
    >>> class Bar(testdata.DictFactory):
    ...     a = testdata.CountingFactory(0)
    ...     b = ConditionalValueField('a', {0: 'a', 1: 'b', 2: 'c'}, -1)
    >>> for i in Bar().generate(3):
    ...     print i
    {'a': 0, 'b': 'a'}
    {'a': 1, 'b': 'b'}
    {'a': 2, 'b': 'c'}
    >>> for i in Bar().generate(4):
    ...     print i
    {'a': 0, 'b': 'a'}
    {'a': 1, 'b': 'b'}
    {'a': 2, 'b': 'c'}
    {'a': 3, 'b': -1}
    """
    def __init__(self, other_field, possible_values, default_value):
        super(ConditionalValueField, self).__init__([other_field])
        self._other_field = other_field
        self._possible_values = possible_values
        self._default_value = default_value

    def __call__(self):
        other_field_value = self.depending_fields[self._other_field] 
        return self._possible_values.get(other_field_value, self._default_value)
