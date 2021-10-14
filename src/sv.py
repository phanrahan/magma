import dataclasses
from typing import List

from mlir import MlirDialect, begin_dialect, end_dialect
from mlir_printer_utils import print_names, print_types
from mlir import MlirOp, MlirRegion, MlirBlock
from mlir import MlirValue
from printer_base import PrinterBase


sv = MlirDialect("sv")
begin_dialect(sv)


@dataclasses.dataclass
class RegOp(MlirOp):
    results: List[MlirValue]
    name: str

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = sv.reg {{name = \"{self.name}\"}} : ")
        print_types(self.results, printer)


@dataclasses.dataclass
class ReadInOutOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = sv.read_inout ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands, printer)


@dataclasses.dataclass
class PAssignOp(MlirOp):
    operands: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        printer.print(f"sv.passign ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands[1], printer)

    
@dataclasses.dataclass
class AlwaysFFOp(MlirOp):
    operands: List[MlirValue]

    def __post_init__(self):
        self.regions.append(MlirRegion())
        self.regions[0].blocks.append(MlirBlock())
        self._block = self.regions[0].blocks[0]

    def add_operation(self, operation: MlirOp):
        self._block.operations.append(operation)

    def print_op(self, printer: PrinterBase):
        printer.print("sv.alwaysff(posedge ")
        print_names(self.operands, printer)
        printer.print(")")


end_dialect()
