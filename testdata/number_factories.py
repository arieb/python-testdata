import random

from .base_factories import Factory

class RandomNumber(Factory):
    def __init__(self, maximum=0, minimum=0, element_amount=0):
        super(RandomInteger, self).__init__(element_amount)
        self._minimum = minimum
        self._maximum = maximum

class RandomInteger(RandomNumber):
    def __call__(self):
        return random.randint(self._maximum, self._minimum)

class RandomFloat(RandomNumber):
    def __call__(self):
        return (random.random() * (self._maximum - self._minimum)) + self._minimum
