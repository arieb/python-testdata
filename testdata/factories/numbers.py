import random

from ..base import Factory, DependentField

class RandomNumber(Factory):
    def __init__(self, minimum=0, maximum=0):
        super(RandomNumber, self).__init__()
        self._minimum = minimum
        self._maximum = maximum

class RandomInteger(RandomNumber):
    def __call__(self):
        return random.randint(self._minimum, self._maximum)

class RandomFloat(RandomNumber):
    def __call__(self):
        return (random.random() * (self._maximum - self._minimum)) + self._minimum

class RelativeNumber(DependentField):
    def __init__(self, other_number_field, delta):
        super(RelativeNumber, self).__init__([other_number_field])
        self._other_number_field = other_number_field
        self._delta = delta
    
    def __call__(self):
        super(RelativeNumber, self).__call__()
        return self.depending_fields[self._other_number_field] + self._delta
