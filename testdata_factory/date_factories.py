import random
import datetime

from .base_factories import Factory

class RandomDateFactory(Factory):
    def __init__(self, maximum, minimum, element_amount=0):
        super(RandomDateFactory, self).__init__(element_amount)
        self._maximum = maximum 
        self._minimum = minimum 
        delta = maximum - minimum
        self._delta_seconds = delta.total_seconds()
        self._sign = -1 if self._delta_seconds < 0 else 1
        self._delta_seconds *= self._sign

    def __call__(self):
        delta = datetime.timedelta(seconds=(random.random() * self._delta_seconds)) 
        return self._minimum + (self._sign * delta)

class DateIntervalFactory(Factory):
    def __init__(self, base, delta, element_amount=0):
        super(DateIntervalFactory, self).__init__(element_amount)
        self._base = base
        self._delta = delta

    def __call__(self):
        return self._base + self.current_index * self._delta

