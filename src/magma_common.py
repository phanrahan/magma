from typing import Any, Callable, Union

import magma as m

from common import make_unique_name, replace_all


ModuleLike = Union[m.DefineCircuitKind, m.Circuit]


_VALUE_OR_TYPE_TO_STRING_REPLACEMENTS = {
    "(": "_",
    ")": "",
    "[": "_",
    "]": "",
    " ": "",
    ",": "_",
    "=": "_",
    ".": "_",
}


def value_or_type_to_string(value_or_type: Union[m.Type, m.Kind]):
    s = str(value_or_type)
    return replace_all(s, _VALUE_OR_TYPE_TO_STRING_REPLACEMENTS)


def make_instance(defn: m.circuit.CircuitKind, **kwargs) -> m.Circuit:
    insts = []

    class _(m.Circuit):
        i = defn(name=f"{defn.name}_{make_unique_name()}", **kwargs)
        insts.append(i)

    return insts[0]


def visit_value_by_direction(
        value: m.Type,
        input_visitor: Callable[[m.Type], Any],
        output_visitor: Callable[[m.Type], Any]):
    if value.is_input():
        return input_visitor(value)
    if value.is_output():
        return output_visitor(value)
    if value.is_mixed():
        if isinstance(value, m.Product):
            for field in value.values():
                visit_value_by_direction(field, input_visitor, output_visitor)
            return
        if isinstance(value, m.Array):
            for item in value:
                visit_value_by_direction(item, input_visitor, output_visitor)
            return
    raise TypeError(value)
