import itertools
import random

from ..base import Factory

class CycleSequenceFactory(Factory):
    """
    Returns the next item in the sequence, constantly cycling between
    all the items.

    Example,
    >>> for i in CycleSequenceFactory([1, 2, 3], 9):
    ...     print i
    1
    2
    3
    1
    2
    3
    1
    2
    3
    """
    def __init__(self, sequence, element_amount=0):
        super(CycleSequenceFactory, self).__init__(element_amount)
        self._cycle_iterator = itertools.cycle(sequence)

    def __call__(self):
        return self._cycle_iterator.next()

class RandomSelection(Factory):
    """
    Randomly chooses an element for the give sequence.

    Example,
    >>> possible_values = set([1, 2, 3])
    >>> while possible_values:
    ...     for i in RandomSelection([1, 2, 3], 100):
    ...         possible_values.discard(i)
    >>> print possible_values
    set([])
    """
    def __init__(self, sequence, element_amount=0):
        super(RandomSelection, self).__init__(element_amount)
        self._sequence = sequence

    def __call__(self):
        return random.choice(self._sequence)

class CountingFactory(Factory):
    """
    Counts from the `start_value` with the give step.

    Example:
    >>> [i for i in CountingFactory(10, 1, 5)]
    [10, 11, 12, 13, 14]
    >>> [i for i in CountingFactory(1, 2, 5)]
    [1, 3, 5, 7, 9]
    """
    def __init__(self, start_value=0, step=1, element_amount=0):
        super(CountingFactory, self).__init__(element_amount)
        self._start_value = start_value
        self._step = step

    def __call__(self):
        return self._start_value + (self._step * self.current_index)
