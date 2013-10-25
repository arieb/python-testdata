from .base_factories import Factory
from .errors import NoSuchDatatype
import faker

class FakeDataFactory(Factory):

    _FAKER_FACTORY = faker.Factory.create()
    
    def __init__(self, data_type, element_amount=0):
        super(FakeDataFactory, self).__init__(element_amount)
        if not hasattr(self._FAKER_FACTORY, data_type):
            raise NoSuchDatatype(data_type)
        self._data_type = data_type
        self._faker_func = getattr(self._FAKER_FACTORY, data_type)

    def __call__(self):
        return self._faker_func()
