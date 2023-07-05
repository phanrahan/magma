import dataclasses
import pathlib

from magma.backend.mlir.mlir import (
    begin_dialect,
    end_dialect,
    MlirAttribute,
    MlirBlock,
    MlirDialect,
    MlirLocation,
    MlirOp,
    MlirRegion,
    MlirType,
)
from magma.backend.mlir.mlir_printer_utils import print_attr_dict
from magma.backend.mlir.print_opts import PrintOpts
from magma.backend.mlir.printer_base import PrinterBase
from magma.config import config, RuntimeConfig


# TODO(rsetaluri): This global runtime config is really somewhat of a hack. This
# should really be a pass or a compile-time option.
config.register(mlir_emit_loc_filename_only=RuntimeConfig(False))

builtin = MlirDialect("builtin")
begin_dialect(builtin)


class UnknownLoc(MlirLocation):
    def emit(self) -> str:
        return "loc(unknown)"


@dataclasses.dataclass(frozen=True)
class FileLineColLoc(MlirLocation):
    file: str
    line: int
    col: int

    def emit(self) -> str:
        path = pathlib.Path(self.file)
        if config.mlir_emit_loc_filename_only:
            path = path.name
        return f"loc(\"{path}\":{self.line}:{self.col})"


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


@dataclasses.dataclass(frozen=True)
class BoolAttr(MlirAttribute):
    value: bool

    def emit(self) -> str:
        return "true" if self.value else "false"


@dataclasses.dataclass(frozen=True)
class StringAttr(MlirAttribute):
    value: str

    def emit(self) -> str:
        return f"\"{self.value}\""


@dataclasses.dataclass
class ModuleOp(MlirOp):
    def __post_init__(self):
        self._block = self.new_region().new_block()

    @property
    def block(self) -> MlirBlock:
        return self._block

    def add_operation(self, operation: MlirOp):
        self._block.add_operation(operation)

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        printer.print("module")
        if self.attr_dict:
            printer.print(" attributes ")
            print_attr_dict(self.attr_dict, printer)


end_dialect()
