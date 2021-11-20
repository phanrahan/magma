import dataclasses

from mlir import MlirDialect, begin_dialect, end_dialect
from mlir import MlirOp, MlirRegion, MlirBlock
from mlir import MlirType
from printer_base import PrinterBase


builtin = MlirDialect("builtin")
begin_dialect(builtin)


@dataclasses.dataclass(frozen=True)
class IntegerType(MlirType):
    n: int

    def emit(self) -> str:
        return f"i{self.n}"


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
