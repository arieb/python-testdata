import random

from ..base import Factory, DependentField

class RandomNumber(Factory):
    """
    A base factory for generating a number between `minimum` and `maximum`.
    """
    def __init__(self, minimum=0, maximum=0):
        super(RandomNumber, self).__init__()
        self._minimum = minimum
        self._maximum = maximum

class RandomInteger(RandomNumber):
    """
    Returns an Integer between `minimum` and `maximum`
    """
    def __call__(self):
        return random.randint(self._minimum, self._maximum)

class RandomFloat(RandomNumber):
    """
    Returns a Float between `minimum` and `maximum`
    """
    def __call__(self):
        return (random.random() * (self._maximum - self._minimum)) + self._minimum

class RelativeNumber(DependentField):
    """
    Returns a number relative to another number field.

    Example:
    >>> import testdata
    >>> class Foo(testdata.DictFactory):
    ...     a = testdata.CountingFactory(1)
    ...     b = RelativeNumber('a', 1)
    >>> [i for i in Foo().generate(3)]
    [{'a': 1, 'b': 2}, {'a': 2, 'b': 3}, {'a': 3, 'b': 4}]
    """
    def __init__(self, other_number_field, delta):
        super(RelativeNumber, self).__init__([other_number_field])
        self._other_number_field = other_number_field
        self._delta = delta
    
    def __call__(self):
        super(RelativeNumber, self).__call__()
        return self.depending_fields[self._other_number_field] + self._delta
