import itertools
import random

from .base_factories import Factory

class CycleSequenceFactory(Factory):
    def __init__(self, sequence, element_amount=0):
        super(CycleSequenceFactory, self).__init__(element_amount)
        self._cycle_iterator = itertools.cycle(sequence)

    def __call__(self):
        return self._cycle_iterator()

class RondomSequenceFactory(Factory):
    def __init__(self, sequence, element_amount=0):
        super(RondomSequenceFactory, self).__init__(element_amount)
        self._sequence = sequence

    def __call__(self):
        return random.choice(self._sequence)

