try:
    import pymongo
except ImportError, import_err:
    raise ImportError("{}. in order to use the mongodb extra you must install pymongo (pip install pymongo)".format(str(import_err)))

from ..factories.sequences import RandomSelection

class FieldFromCollection(RandomSelection):
    """
    Querys a MongoDB collection for all the possible values of `field_name`, and constantly
    returns a random result.

    Note:
    When creating a new FieldFromCollection, the database is queried. If you already
    have a list of results, you might want to use the `RandomSelection` Factory directly.

    :param database: The name of the database to connect to.
    :param collection: The name of the collection inside the database to connect to.
    :param field_name: The field in the collection we want to get the values from.
    :param filter_query: A filter to pass to the pymongo.Collection's find function.
    :param **connection_kw - The parameters that are passed to the pymongo.MongoClient __init__ function.
    """
    def __init__(self, database, collection, field_name, filter_query={}, **connection_kw):
        with pymongo.MongoClient(**connection_kw) as client:
            db = client[database]
            collection = db[collection]
            possible_values = collection.find(filter_query).distinct(field_name)
        super(FieldFromCollection, self).__init__(possible_values)
