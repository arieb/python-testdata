import random
import string
from .base_factories import Factory


class RandomLengthStringFactory(Factory):

    MIN_CHAR_DEFAULT = 3
    MAX_CHAR_DEFAULT = 100

    def __init__(self, min_chars=None, max_chars=None, prefix=None, suffix=None, generation=0, element_amount=0):
        super(RandomLengthStringFactory, self).__init__(generation, element_amount)

        self._min_chars = min_chars if min_chars else self.MIN_CHAR_DEFAULT
        self._max_chars = max_chars if max_chars else self.MAX_CHAR_DEFAULT
        self._prefix = prefix if prefix else ''
        self._suffix = suffix if suffix else ''

        if type(self._min_chars) != int:
            raise TypeError("min_chars needs to be an integer")
        if type(self._max_chars) != int:
            raise TypeError("max_chars needs to be an integer")

    def __call__(self):
        length = random.randint(self._min_chars, self._max_chars)
        random_string = [random.choice(string.ascii_letters) for i in xrange(length)]
        random_string.insert(0, self._prefix)
        random_string.append(self._suffix)

        return ''.join(random_string)
