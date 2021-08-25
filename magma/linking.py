from typing import Mapping, Optional

from magma.circuit import CircuitKind


_link_map = {}


def link_module(source: CircuitKind, key: str, target: CircuitKind):
    global _link_map
    targets = _link_map.setdefault(source, dict())
    targets[key] = target


def get_linked_modules(source: CircuitKind) -> Mapping[str, CircuitKind]:
    global _link_map
    targets = _link_map.setdefault(source, dict())
    return targets


def clear_linked_modules(source: Optional[CircuitKind] = None):
    """
    Clears all linked modules if @source is None, otherwise clears the modules
    for the specified module.
    """
    global _link_mxoap
    if source is None:
        _link_map.clear()
        return
    try:
        del _link_map[source]
    except KeyError:
        pass
