from collections import defaultdict
from .errors import UnmetDependentFields, NoFactoriesDefined

from .base import Factory, DependentField

class DictFactoryBuilder(type):
    """
    A metaclass that builds DictFactory based classes.
    """
    def __new__(meta, name, bases, dct):
        if name == "DictFactory": # we only modify the children of DictFactory, not the DictFactory itself
            return super(DictFactoryBuilder, meta).__new__(meta, name, bases, dct)

        _child_factory_tree = DictFactoryBuilder._collect_bases_children_trees(bases)
        DictFactoryBuilder._build_children_tree(_child_factory_tree, dct)
        DictFactoryBuilder._clean_factories(dct)
        dct["_child_factory_tree"] = _child_factory_tree
        return super(DictFactoryBuilder, meta).__new__(meta, name, bases, dct)

    @staticmethod
    def _collect_bases_children_trees(bases):
        all_tree = defaultdict(dict)
        for base in bases:
            if Factory in base.__bases__: # means we reached the DictFactory cls
                return defaultdict(dict)
            current_tree = DictFactoryBuilder._fuse_child_trees(
                    base._child_factory_tree,
                    DictFactoryBuilder._collect_bases_children_trees(base.__bases__))
            DictFactoryBuilder._fuse_child_trees(all_tree, current_tree)
        return all_tree

    @staticmethod
    def _fuse_child_trees(p,q):
        for key in q.keys():
            p[key].update(q[key])
        return p

    @staticmethod
    def _clean_factories(dct):
        """
        After we create the children factory, we don't need it anymore
        """
        for key in dct.keys():
            if issubclass(type(dct[key]), Factory):
                del dct[key]

    @staticmethod
    def _build_children_tree(child_tree, dct):
        dependent_factories = {}
        for key, value in dct.iteritems():
            if issubclass(type(value), DependentField):
                dependent_factories[key] = value
                continue
            if issubclass(type(value), Factory):
                child_tree[0][key] = value
        if not child_tree:
            raise NoFactoriesDefined("DictFactory needs to contain at least one Factory")
        DictFactoryBuilder._build_dependency_tree(child_tree, dependent_factories)
    
    @staticmethod
    def _build_dependency_tree(child_tree, dependent_factories):
        leftover_factories = set(dependent_factories.keys())
        unplaced_fields = set()
        while leftover_factories:
            unplaced_fields = DictFactoryBuilder._build_tree(child_tree, leftover_factories, dependent_factories)
            if unplaced_fields == leftover_factories: # means that no placement has happened!
                raise UnmetDependentFields("The fields: {} - depend on fields that aren't defined!".format(unplaced_fields))
            leftover_factories = unplaced_fields 

    @staticmethod
    def _build_tree(child_tree, leftover_factory_names, all_dependent_factories):
        unplaced_fields = set([])
        for factory_name in leftover_factory_names:
            needed_factories = set(all_dependent_factories[factory_name].depending_field_names) # we need to know which fields are needed
            for generation in sorted(child_tree.keys()): # will give the available generations
                needed_factories -= set(child_tree[generation].keys()) # the factory names available in this generation 
                if not needed_factories:
                    break
            if needed_factories: # if after traversing the generations, we didn't find all the dependencies, we save this for later
                unplaced_fields.add(factory_name)
            else:
                child_tree[generation + 1][factory_name] = all_dependent_factories[factory_name]
        return unplaced_fields

