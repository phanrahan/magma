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
    return


class ElaborateTuplesPass(DefinitionPass):
    def __call__(self, definition):
        with definition.open():
            for value in definition.interface.ports.values():
                if _is_tuple_or_nested_tuple(type(value)):
                    _expand(value)
            for instance in definition.instances:
                for value in instance.interface.ports.values():
                    if _is_tuple_or_nested_tuple(type(value)):
                        _expand(value)


elaborate_tuples = pass_lambda(ElaborateTuplesPass)
