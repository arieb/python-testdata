class TestDataError(Exception): pass
class MissingElementAmountValue(TestDataError): pass
class FactoryStartedAlready(TestDataError): pass
class NoSuchDatatype(TestDataError): pass
class NoSuchOlderField(TestDataError): pass
class InvalidFieldType(TestDataError): pass
