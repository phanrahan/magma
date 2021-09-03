from typing import Iterable, Mapping, Optional

from magma.circuit import CircuitKind


class _LinkInfo:
    def __init__(self):
        self.default_linked_module = None
        self.linked_modules = {}


_link_map = {}


def _get_or_create_link_info(source: CircuitKind) -> _LinkInfo:
    global _link_map
    return _link_map.setdefault(source, _LinkInfo())


def link_module(source: CircuitKind, key: str, target: CircuitKind):
    # TODO(rsetaluri): Catch errors early here?
    info = _get_or_create_link_info(source)
    info.linked_modules[key] = target


def get_linked_modules(source: CircuitKind) -> Mapping[str, CircuitKind]:
    info = _get_or_create_link_info(source)
    return info.linked_modules


def link_default_module(source: CircuitKind, target: CircuitKind):
    # TODO(rsetaluri): Catch errors early here?
    info = _get_or_create_link_info(source)
    info.default_linked_module = target


def has_default_linked_module(source: CircuitKind) -> bool:
    info = _get_or_create_link_info(source)
    return info.default_linked_module is not None


def get_default_linked_module(source: CircuitKind) -> CircuitKind:
    info = _get_or_create_link_info(source)
    return info.default_linked_module


def has_any_linked_modules(source: CircuitKind) -> bool:
    return has_default_linked_module(source) or get_linked_modules(source)


def get_all_linked_modules(source: CircuitKind) -> Iterable[CircuitKind]:
    targets = []
    if has_default_linked_module(source):
        targets += [get_default_linked_module(source)]
    return targets + list(get_linked_modules(source).values())


def clear_link_info(source: Optional[CircuitKind] = None):
    """
    Clears all linked modules if @source is None, otherwise clears the modules
    for the specified module.
    """
    global _link_map
    if source is None:
        _link_map.clear()
        return
    try:
        del _link_map[source]
    except KeyError:
        pass
