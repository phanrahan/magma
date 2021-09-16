import abc
import dataclasses


class MlirType(abc.ABC):
    @abc.abstractmethod
    def emit(self) -> str:
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class MlirIntegerType(MlirType):
    n: int

    def emit(self) -> str:
        return f"i{self.n}"
