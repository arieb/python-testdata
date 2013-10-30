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

    @property
    def element_amount(self):
        return self._element_amount
    
    def set_element_amount(self, new_element_amount):
        if self._has_started:
            raise FactoryStartedAlready("can't change 'element_amount' if factory has started")
        self._element_amount = new_element_amount

    @property
    def precent(self):
        return (float(self.current_index) / float(self.element_amount)) * 100

class DictFactory(Factory):
    def __init__(self, element_amount=0):
        super(DictFactory, self).__init__(element_amount)
        self._child_factories = {}
        self._build_child_factories()
        self.set_element_amount(element_amount)

    def __iter__(self):
        self._iter_child_factories()
        return self

    def _build_child_factories(self):
        for key, value in self.__class__.__dict__.iteritems():
            if issubclass(type(value), Factory):
                self._child_factories[key] = value

    def _iter_child_factories(self):
        for key in self._child_factories.copy().keys():
            self._child_factories[key] = iter(self._child_factories[key])

    def __call__(self):
        result = {}
        for factory_name, factory in self._child_factories.iteritems():
           result[factory_name] = factory() 

        return result

    def increase_index(self):
        super(DictFactory, self).increase_index()
        for child_factory in self._child_factories.values():
            child_factory.increase_index()
    
    def set_element_amount(self, new_element_amount):
        super(DictFactory, self).set_element_amount(new_element_amount)
        for child_factory in self._child_factories.values():
            child_factory.set_element_amount(new_element_amount)

class ListFactory(Factory):
    def __init__(self, element_amount=0, factory_class=None, elements_per_list=0):
        super(ListFactory, self).__init__(element_amount)
        self._factory = iter(factory_class(element_amount * elements_per_list))
        self._elements_per_list = elements_per_list

    def __call__(self):
        return [self._factory.next() for i in xrange(self._elements_per_list)]

class Callable(Factory):
    """
    A basic factory that returns the result of a call to `callable_obj`s __call__ function
    :param callable_obj: an object that implements the __call__ method
    :param element_amount: the amount of elements this factory will create.

    Example:
    >>> list(Callable(lambda: 'foo', 4))
    ['foo', 'foo', 'foo', 'foo']
    """
    def __init__(self, callable_obj, element_amount=0):
        super(Callable, self).__init__(element_amount)
        self._callable_obj = callable_obj

    def __call__(self):
        return self._callable_obj()

