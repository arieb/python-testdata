from .sequence_factories import RandomSelection

class FieldFromCollection(RandomSelection):
    def __init__(self, collection, field_name, filter_query={}, generation=0, element_amount=0):
        self._collection = collection
        self._field_name = field_name
        possible_values = collection.find(filter_query).distinct(field_name)
        super(FieldFromCollection, self).__init__(possible_values, generation, element_amount)
