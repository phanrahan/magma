import dataclasses
from typing import Union

from mlir_type import MlirType


_anonymous_index = 0


# NOTE(rsetaluri): We need instances of this class to have predictable,
# consistent, and distinct string representations. We use a global counter to
# achieve this. These properties are needed downstream; in particular in cases
# where hashes are used to distinguish graph nodes, and to have str() be a
# consistently ordered key for nodes (see comment in cycle breaking pass).
@dataclasses.dataclass(frozen=True)
class _Anonymous:
    key: int


def _make_anonymous() -> _Anonymous:
    global _anonymous_index
    key = _anonymous_index
    _anonymous_index += 1
    return _Anonymous(key)


@dataclasses.dataclass(frozen=True)
class MlirValue:
    type: MlirType
    name: Union[str, _Anonymous] = dataclasses.field(default_factory=_make_anonymous)


def mlir_value_is_anonymous(value: MlirValue) -> bool:
    if not isinstance(value, MlirValue):
        raise TypeError(value)
    return isinstance(value.name, _Anonymous)
