from magma.passes.passes import DefinitionPass, pass_lambda
from magma.tuple import Tuple
from magma.array import Array


def _is_tuple_or_nested_tuple(T):
    if issubclass(T, Tuple):
        return True
    if issubclass(T, Array):
        return _is_tuple_or_nested_tuple(T.T)
    return False


def _expand(value):
    if isinstance(value, Tuple):
        for elem in value:
            _expand(elem)
    if isinstance(value, Array) and _is_tuple_or_nested_tuple(type(value)):
        for elem in value:
            _expand(elem)


def _expand_tuple_values(values):
    for value in values:
        if _is_tuple_or_nested_tuple(type(value)):
            _expand(value)


class ElaborateTuplesPass(DefinitionPass):
    def __call__(self, definition):
        with definition.open():
            _expand_tuple_values(definition.interface.ports.values())
            for instance in definition.instances:
                _expand_tuple_values(instance.interface.ports.values())


elaborate_tuples = pass_lambda(ElaborateTuplesPass)
