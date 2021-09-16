import dataclasses

from mlir_type import MlirType


@dataclasses.dataclass(frozen=True)
class MlirValue:
    name: str
    type: MlirType
