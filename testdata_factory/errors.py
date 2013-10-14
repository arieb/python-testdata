class MongoFactoryError(Exception): pass
class MissingElementAmountValue(MongoFactoryError): pass
class FactoryStartedAlready(MongoFactoryError): pass
