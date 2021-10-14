from typing import Union

import magma as m

from common import make_unique_name


ModuleLike = Union[m.DefineCircuitKind, m.Circuit]


def make_type_string(T: m.Kind):
    _REPLACEMENTS = (
        ("(", "_"), (")", ""), ("[", "_"), ("]", ""), (" ", ""), (",", "_"),
        ("=", "_"))
    s = str(T)
    for old, new in _REPLACEMENTS:
        s = s.replace(old, new)
    return s


def make_instance(defn: m.circuit.CircuitKind, **kwargs) -> m.Circuit:
    insts = []

    class _(m.Circuit):
        i = defn(name=make_unique_name(), **kwargs)
        insts.append(i)

    return insts[0]


