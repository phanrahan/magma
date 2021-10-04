import abc
import dataclasses
from typing import Tuple


class MlirType(abc.ABC):
    @abc.abstractmethod
    def emit(self) -> str:
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class MlirIntegerType(MlirType):
    n: int

    def emit(self) -> str:
        return f"i{self.n}"


@dataclasses.dataclass(frozen=True)
class HwArrayType(MlirType):
    dims: Tuple[int]
    T: MlirType

    def emit(self) -> str:
        dim_str = "x".join(map(str, self.dims))
        return f"!hw.array<{dim_str}x{self.T.emit()}>"


@dataclasses.dataclass(frozen=True)
class HwStructType(MlirType):
    fields: Tuple[Tuple[str, MlirType]]

    def emit(self) -> str:
        field_str = ", ".join(f"{k}: {t.emit()}" for k, t in self.fields)
        return f"!hw.struct<{field_str}>"


@dataclasses.dataclass(frozen=True)
class HwInOutType(MlirType):
    T: MlirType

    def emit(self) -> str:
        return f"!hw.inout<{self.T.emit()}>"
