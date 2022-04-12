import dataclasses

from magma.backend.mlir.mlir import MlirDialect, begin_dialect, end_dialect
from magma.backend.mlir.mlir import MlirAttribute
from magma.backend.mlir.mlir import MlirOp, MlirRegion, MlirBlock
from magma.backend.mlir.mlir import MlirType
from magma.backend.mlir.printer_base import PrinterBase


builtin = MlirDialect("builtin")
begin_dialect(builtin)


@dataclasses.dataclass(frozen=True)
class IntegerType(MlirType):
    n: int

    def emit(self) -> str:
        return f"i{self.n}"


@dataclasses.dataclass(frozen=True)
class IntegerAttr(MlirAttribute):
    value: int

    def emit(self) -> str:
        return str(self.value)


@dataclasses.dataclass
class ModuleOp(MlirOp):
    def __post_init__(self):
        self._block = self.new_region().new_block()

    @property
    def block(self) -> MlirBlock:
        return self._block

    def add_operation(self, operation: MlirOp):
        self._block.add_operation(operation)

    def print_op(self, printer: PrinterBase):
        printer.print("module")


end_dialect()
