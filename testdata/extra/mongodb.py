from ..factories.sequences import RandomSelection

class FieldFromCollection(RandomSelection):
    def __init__(self, collection, field_name, filter_query={}, element_amount=0):
        self._collection = collection
        self._field_name = field_name
        possible_values = collection.find(filter_query).distinct(field_name)
        super(FieldFromCollection, self).__init__(possible_values, element_amount)
