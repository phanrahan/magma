import dataclasses
from typing import List

from mlir_value import MlirValue


@dataclasses.dataclass(frozen=True)
class MlirOp:
    name: str


@dataclasses.dataclass(frozen=True)
class CombOp(MlirOp):
    name: str
    op: str

    def emit(self):
        return (f"{{output_names}} = comb.{self.op} {{input_names}} : "
                f"{{output_types}}")


@dataclasses.dataclass(frozen=True)
class HwOutputOp(MlirOp):
    name: str

    def emit(self):
        return (f"hw.output {{input_names}} : {{input_types}}")
