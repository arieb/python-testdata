from copy import deepcopy, copy
from .base import Factory
from .metaclasses import DictFactoryBuilder

class DictFactory(Factory):
    """
    One of the most useful and basic factories.
    This factory is meant to be subclassed, and other factories should be defined
    as class variables.
    This factory is used to generate dictonaries which have the results of the factories
    it contains as keys and values.

    Example:
    >>> import testdata
    >>> class Users(DictFactory):
    ...    id = testdata.CountingFactory(10)
    ...    age = testdata.RandomInteger(10, 10) 
    ...    gender = testdata.RandomSelection(['male'])
    >>> [result] = [i for i in Users().generate(1)]
    >>> result
    {'gender': 'male', 'age': 10, 'id': 10}
    """
    __metaclass__ = DictFactoryBuilder

    def __init__(self, **factories):
        super(DictFactory, self).__init__()
        self._child_factories = deepcopy(self._child_factory_tree)
        self._child_factories.update(factories)
        self._oldest_generation = max(self._child_factories.keys())

    def __iter__(self):
        self._iter_child_factories()
        return self

    def _iter_child_factories(self):
        child_factories = copy(self._child_factories)
        for generation in child_factories.keys():
            for key in child_factories[generation].keys(): 
                self._child_factories[generation][key] = iter(child_factories[generation][key])

    def _get_oldest_generation(self):
        return max(self._child_factories.keys())

    def __call__(self):
        result = {}
        for factory_name, factory in self._child_factories[0].iteritems():
            result[factory_name] = factory() 

        # now we call all Factories subclassing the DependentField
        for i in xrange(1, self._oldest_generation + 1):
            generation_result = {}
            for factory_name, factory in self._child_factories[i].iteritems():
                factory.update_depending(result)
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
