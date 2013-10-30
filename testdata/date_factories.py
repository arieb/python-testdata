import random
import datetime

from .base_factories import Factory

class RandomDateFactory(Factory):
    """
    Generates a random dates between 2 dates.
    """
    def __init__(self, minimum, maximum, element_amount=0):
        """
        Constucts the RandomDateFactory.
        :type minimum: datetime.datetime
        :type maximum: datetime.datetime
        :type element_amount: int
        
        Example:
        >>> f = list(RandomDateFactory(datetime.datetime(2013, 10, 1, 1, 1, 0, 0), datetime.datetime(2013, 10, 1, 1, 1, 0, 1), 100))
        >>> len(f)
        100
        >>> datetime.datetime(2013, 10, 1, 1, 1, 0, 0) in f
        True
        >>> datetime.datetime(2013, 10, 1, 1, 1, 0, 1) in f
        True
        >>> datetime.datetime(2013, 10, 1, 1, 1, 0, 2) in f
        False
        >>> datetime.datetime(2013, 10, 1, 2, 1, 0, 2) in f
        False
        """
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
    """
    Generates datetime objects starting from `base` which each iteration adding `delta` to it.
    :type base: datetime.datetime
    :type delta: datetime.timedelta

    Example:
    >>> list(DateIntervalFactory(datetime.datetime(2013, 10, 1), datetime.timedelta(days=1), 3))
    [datetime.datetime(2013, 10, 1, 0, 0), datetime.datetime(2013, 10, 2, 0, 0), datetime.datetime(2013, 10, 3, 0, 0)]
    """
    def __init__(self, base, delta, element_amount=0):
        super(DateIntervalFactory, self).__init__(element_amount)
        self._base = base
        self._delta = delta

    def __call__(self):
        return self._base + self.current_index * self._delta

