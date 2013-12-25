from collections import defaultdict

from .errors import UnmetDependentFields
from .base import Factory, DependentField

class ChildrenTree(object):
    def __init__(self):
        self._tree = defaultdict(dict)

    def load_bases(self, bases):
        ChildrenTree._fuse_tree(self._tree, ChildrenTree._load_bases(bases))

    @staticmethod
    def _load_bases(bases):
        all_tree = ChildrenTree()
        for base in bases:
            if Factory == base: # means we reached the DictFactory cls
                return ChildrenTree()
            current_tree = base._child_factory_tree + ChildrenTree._load_bases(base.__bases__)
            all_tree += current_tree
        return all_tree

    @staticmethod
    def _fuse_tree(a, b):
        for key in b.keys():
            a[key].update(b[key])

    def __add__(self, other):
        new_tree = self._tree.copy()
        ChildrenTree._fuse_tree(new_tree, other._tree)
        new_children_tree = ChildrenTree()
        new_children_tree._tree = new_tree
        return new_children_tree

    def __iadd__(self, o):
        ChildrenTree._fuse_tree(self._tree, o._tree)
        return self

    def __repr__(self):
        return '{}'.format(repr(self._tree))

    def keys(self):
        return self._tree.keys()
    
    def __getitem__(self, key):
        return self._tree.__getitem__(key)

    def update(self, factories_dct):
        dependent_factories = {}
        for key, value in factories_dct.iteritems():
            if issubclass(type(value), DependentField):
                dependent_factories[key] = value
                continue
            if issubclass(type(value), Factory):
                self._tree[0][key] = value

        self._build_dependency_tree(dependent_factories)
    
    def _build_dependency_tree(self, dependent_factories):
        leftover_factories = set(dependent_factories.keys())
        unplaced_fields = set()
        while leftover_factories:
            unplaced_fields = self._build_tree(leftover_factories, dependent_factories)
            if unplaced_fields == leftover_factories: # means that no placement has happened!
                raise UnmetDependentFields("The fields: {} - depend on fields that aren't defined!".format(unplaced_fields))
            leftover_factories = unplaced_fields 

    def _build_tree(self, leftover_factory_names, all_dependent_factories):
        unplaced_fields = set([])
        for factory_name in leftover_factory_names:
            needed_factories = set(all_dependent_factories[factory_name].depending_field_names) # we need to know which fields are needed
            for generation in sorted(self._tree.keys()): # will give the available generations
                needed_factories -= set(self._tree[generation].keys()) # the factory names available in this generation 
                if not needed_factories:
                    break
            if needed_factories: # if after traversing the generations, we didn't find all the dependencies, we save this for later
                unplaced_fields.add(factory_name)
            else:
                self._tree[generation + 1][factory_name] = all_dependent_factories[factory_name]
        return unplaced_fields
