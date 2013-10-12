from .errors import MissingElementAmountValue, FactoryStartedAlready

class Factory(object):
    def __init__(self, element_amount = 0):
        self._element_amount = element_amount
        self._current_index = 0
        self._has_started = False

    def __iter__(self):
        if not self._element_amount:
            raise MissingElementAmountValue("missing element_amount for {}".format(self.__class__))
        self._has_started = True
        
        return self
    
    def next(self):
        if self.current_index >= self.element_amount:
            raise StopIteration

        value = self()
        self.increase_index()

        return value

    def increase_index(self):
        self._current_index += 1

    def __call__(self):
        raise NotImplementedError()

    @property
    def current_index(self):
        return self._current_index

    def _get_element_amount(self):
        return self._element_amount
    
    def _set_element_amount(self, new_element_amount):
        if self._has_started:
            raise FactoryStartedAlready("can't change 'element_amount' if factory has started")
        self._element_amount = new_element_amount

    @property
    def precent(self):
        return (float(self.current_index) / float(self.element_amount)) * 100

    element_amount = property(_get_element_amount, _set_element_amount)


class DictFactory(Factory):
    def __init__(self, element_amount=0):
        super(DictFactory, self).__init__(element_amount)
        self._child_factories = {}
        self._build_child_factories()

    def _build_child_factories(self):
        for key, value in self.__class__.__dict__.iteritems():
            if issubclass(type(value), Factory):
                value.element_amount = self.element_amount
                self._child_factories[key] = iter(value)

    def __call__(self):
        result = {}
        for factory_name, factory in self._child_factories.iteritems():
           result[factory_name] = factory() 

        return result

    def increase_index(self):
        super(DictFactory, self).increase_index()
        for child_factory in self._child_factories.values():
            child_factory.increase_index()
