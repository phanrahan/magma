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
