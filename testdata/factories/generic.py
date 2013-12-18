from ..base import Factory


class Constant(Factory):
    def __init__(self, constant_value, element_amount=0):
        super(Constant, self).__init__(element_amount)
        self._constant_value = constant_value

    def __call__(self):
        return self._constant_value

class CountingFactory(Factory):
    def __init__(self, start_value=0, element_amount=0):
        super(CountingFactory, self).__init__(element_amount)
        self._start_value = start_value

    def __call__(self):
        return self._start_value + self.current_index
