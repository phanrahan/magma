from magma.passes.passes import DefinitionPass, pass_lambda
from magma.type_utils import contains_tuple


def _expand(value):
    if contains_tuple(type(value)):
        for elem in value:
            _expand(elem)


def _expand_tuple_values(values):
    for value in values:
        if contains_tuple(type(value)):
            _expand(value)


class ElaborateTuplesPass(DefinitionPass):
    def __call__(self, definition):
        with definition.open():
            _expand_tuple_values(definition.interface.ports.values())
            for instance in definition.instances:
                _expand_tuple_values(instance.interface.ports.values())


elaborate_tuples = pass_lambda(ElaborateTuplesPass)
