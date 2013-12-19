from ..base import Factory

class Constant(Factory):
    """
    Returns the same value on each iteration.

    Example,
    >>> [i for i in Constant(1, 5)]
    [1, 1, 1, 1, 1]
    """
    def __init__(self, constant_value, element_amount=0):
        super(Constant, self).__init__(element_amount)
        self._constant_value = constant_value

    def __call__(self):
        return self._constant_value
