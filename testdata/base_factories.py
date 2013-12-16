from collections import defaultdict
from .errors import MissingElementAmountValue, FactoryStartedAlready, NoSuchOlderField

class Factory(object):
    def __init__(self, generation=0, element_amount=0):
        self._element_amount = element_amount
        self._generation = generation
        self._current_index = 0
        self._old_generation_factories = {}
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

    @property
    def generation(self):
        return self._generation

    def set_older_generation(self, other_factories):
        self._old_generation_factories = other_factories

    @property
    def older_generations(self):
        return self._old_generation_factories

class DictFactory(Factory):
    def __init__(self, generation=0, element_amount=0):
        super(DictFactory, self).__init__(generation, element_amount)
        self._child_factories = defaultdict(dict)
        self._build_child_factories()
        self._oldest_generation = self._get_oldest_generation()
        self.set_element_amount(element_amount)

    def _build_child_factories(self):
        for key, value in self.__class__.__dict__.iteritems():
            if issubclass(type(value), Factory):
                self._child_factories[value.generation][key] = value

    def __iter__(self):
        self._iter_child_factories()
        return self

    def _iter_child_factories(self):
        child_factories = self._child_factories.copy()
        for generation in child_factories.keys():
            for key in child_factories[generation].keys(): 
                self._child_factories[generation][key] = iter(child_factories[generation][key])

    def _get_oldest_generation(self):
        return max(self._child_factories.keys())

    def __call__(self):
        result = {}
        for i in xrange(self._oldest_generation + 1):
            generation_result = {}
            for factory_name, factory in self._child_factories[i].iteritems():
                factory.set_older_generation(result)
                generation_result[factory_name] = factory() 

            result.update(generation_result)

        return result

    def increase_index(self):
        super(DictFactory, self).increase_index()
        for i in xrange(self._oldest_generation + 1):
            for child_factory in self._child_factories[i].values():
                child_factory.increase_index()
    
    def set_element_amount(self, new_element_amount):
        super(DictFactory, self).set_element_amount(new_element_amount)
        for i in xrange(self._oldest_generation + 1):
            for child_factory in self._child_factories[i].values():
                child_factory.set_element_amount(new_element_amount)

class ListFactory(Factory):
    """
    A factory that returns on each iteration a list of `elements_per_list` items returned 
    from calls to the given factory.

    Example,
    >>> import testdata
    >>> f = ListFactory(testdata.CountingFactory(1), 0, 5, 3)
    >>> list(f)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]
    """
    def __init__(self, factory=None, generation=0, element_amount=0, elements_per_list=0):
        super(ListFactory, self).__init__(generation, element_amount)
        factory.set_element_amount(element_amount * elements_per_list)
        self._factory = iter(factory)
        self._elements_per_list = elements_per_list

    def __call__(self):
        return [self._factory.next() for i in xrange(self._elements_per_list)]

class Callable(Factory):
    """
    A factory that returns the result of a call to `callable_obj`s __call__ function,
    on each iteration.
    :param callable_obj: an object that implements the __call__ method
    :param element_amount: the amount of elements this factory will create.

    Example:
    >>> list(Callable(lambda: 'foo', 0, 4))
    ['foo', 'foo', 'foo', 'foo']
    """
    def __init__(self, callable_obj, generation=0, element_amount=0):
        super(Callable, self).__init__(generation, element_amount)
        self._callable_obj = callable_obj

    def __call__(self):
        return self._callable_obj()

class ClonedField(Factory):
    """
    A factory that copies the value of another factory.
    Note:
    In order for the ClonedField to work, it needs to be of a high `generation`
    than the cloned field.

    Example:
    >>> import testdata
    >>> class Foo(testdata.DictFactory):
    ...     id = testdata.CountingFactory(0, 0)
    ...     cloned_id = ClonedField("id", 1)
    >>> [result] = [i for i in Foo(0, 1)]
    >>> result['id'] == result['cloned_id']
    True
    >>> class Bar(testdata.DictFactory):
    ...     id = testdata.CountingFactory(0, 0)
    ...     cloned_id = ClonedField("id", 0)
    >>> [result] = [i for i in Bar(0, 1)]
    Traceback (most recent call last):
    NoSuchOlderField: Missing id field in older generation fields
    """
    def __init__(self, cloned_field_name, generation=0, element_amount=0):
        super(ClonedField, self).__init__(generation, element_amount)
        self._cloned_field_name = cloned_field_name

    def __call__(self):
        if not self.older_generations.has_key(self._cloned_field_name):
            raise NoSuchOlderField("Missing {} field in older generation fields".format(self._cloned_field_name))

        return self.older_generations[self._cloned_field_name]
