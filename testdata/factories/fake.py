from ..base import Callable
from ..errors import NoSuchDatatype
import faker

class FakeDataFactory(Callable):

    _FAKER_FACTORY = faker.Factory.create()
    
    def __init__(self, data_type, element_amount=0):
        if not hasattr(self._FAKER_FACTORY, data_type):
            raise NoSuchDatatype(data_type)
        self._data_type = data_type
        faker_func = getattr(self._FAKER_FACTORY, data_type)
        super(FakeDataFactory, self).__init__(faker_func, element_amount)
