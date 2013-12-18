from .errors import MissingElementAmountValue, FactoryStartedAlready, MissingRequiredFields

class Factory(object):
    """
    The base class of all the factories.
    Implementes the core factory logic.
    """
    def __init__(self, element_amount=0):
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


class DependentField(Factory):
    """
    This is the base class of fields that their result depends on the values
    of another field.
    This should be used inside the DictFactory.
    """
    def __init__(self, depending_field_names=[], element_amount=0):
        super(DependentField, self).__init__(element_amount)
        self._depending_field_names = depending_field_names
        self._depending_fields = {}

    def _check_missing_fields(self, required_fields, available_fields):
        missing_fields = set(required_fields) - set(available_fields)
        if missing_fields:
            raise MissingRequiredFields(str(missing_fields))

    def update_depending(self, new_depending_values):
        """
        updates the depending field values.
        The fields should be updated before each call to the factory.
        """
        self._check_missing_fields(set(self._depending_field_names), set(new_depending_values.keys()))

        for field in self._depending_field_names:
            self._depending_fields[field] = new_depending_values[field]

    def __call__(self):
        # if we are missing depending fields values
        self._check_missing_fields(set(self.depending_field_names), set(self._depending_fields.keys())) 

    @property
    def depending_field_names(self):
        return self._depending_field_names

    @property
    def depending_fields(self):
        return self._depending_fields.copy()

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
    def __init__(self, factory=None, element_amount=0, elements_per_list=0):
        super(ListFactory, self).__init__(element_amount)
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
    def __init__(self, callable_obj, element_amount=0):
        super(Callable, self).__init__(element_amount)
        self._callable_obj = callable_obj

    def __call__(self):
        return self._callable_obj()

class ClonedField(DependentField):
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
    def __init__(self, cloned_field_name, element_amount=0):
        super(ClonedField, self).__init__([cloned_field_name], element_amount)
        self._cloned_field_name = cloned_field_name

    def __call__(self):
        super(ClonedField, self).__call__()
        return self.depending_fields[self._cloned_field_name]
