import dataclasses
from typing import Union

from mlir_type import MlirType


class _Anonymous: pass


@dataclasses.dataclass(frozen=True)
class MlirValue:
    type: MlirType
    name: Union[str, _Anonymous] = dataclasses.field(default_factory=_Anonymous)


def mlir_value_is_anonymous(value: MlirValue) -> bool:
    if not isinstance(value, MlirValue):
        raise TypeError(value)
    return isinstance(value.name, _Anonymous)
