import dataclasses
from typing import List, Optional

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
class AssignOp(MlirOp):
    operands: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        printer.print(f"sv.assign ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands[1], printer)


@dataclasses.dataclass
class PAssignOp(MlirOp):
    operands: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        printer.print(f"sv.passign ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands[1], printer)


@dataclasses.dataclass
class BPAssignOp(MlirOp):
    operands: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        printer.print(f"sv.bpassign ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands[1], printer)


@dataclasses.dataclass
class AlwaysFFOp(MlirOp):
    operands: List[MlirValue]
    clock_edge: str
    reset_type: str = None
    reset_edge: str = None

    def __post_init__(self):
        self.regions.append(MlirRegion())
        self.regions[0].blocks.append(MlirBlock())
        self._body_block = self.regions[0].blocks[0]
        if self.reset_type is None:
            return
        self.regions.append(MlirRegion())
        self.regions[1].blocks.append(MlirBlock())
        self._reset_block = self.regions[1].blocks[0]

    @property
    def body_block(self) -> MlirBlock:
        return self._body_block

    @property
    def reset_block(self) -> MlirBlock:
        return self._reset_block

    def print(self, printer: PrinterBase):
        printer.print(f"sv.alwaysff({self.clock_edge} ")
        print_names(self.operands[0], printer)
        printer.print(") {")
        printer.flush()
        printer.push()
        self.body_block.print(printer)
        printer.pop()
        printer.print("}")
        if self.reset_type is None:
            printer.flush()
            return
        printer.print(f" ({self.reset_type} : {self.reset_edge} ")
        print_names(self.operands[1], printer)
        printer.print(") {")
        printer.flush()
        printer.push()
        self.reset_block.print(printer)
        printer.pop()
        printer.print_line("}")

    def print_op(self, printer: PrinterBase):
        printer.print("sv.alwaysff(posedge ")
        print_names(self.operands, printer)
        printer.print(")")


@dataclasses.dataclass
class InitialOp(MlirOp):
    def __post_init__(self):
        self.regions.append(MlirRegion())
        self.regions[0].blocks.append(MlirBlock())
        self._block = self.regions[0].blocks[0]

    def add_operation(self, operation: MlirOp):
        self._block.operations.append(operation)

    def print_op(self, printer: PrinterBase):
        printer.print("sv.initial")


@dataclasses.dataclass
class WireOp(MlirOp):
    results: List[MlirValue]
    name: str
    sym: Optional[str] = None

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(" = sv.wire ")
        if self.sym is not None:
            printer.print(f"sym {self.sym} ")
        printer.print(f"{{name=\"{self.name}\"}} : ")
        print_types(self.results, printer)


@dataclasses.dataclass
class VerbatimOp(MlirOp):
    operands: List[MlirOp]
    string: str

    def print_op(self, printer: PrinterBase):
        # NOTE(rsetaluri): This is a hack to "double-escape" escape characters
        # like `\n`, `\t`.
        string = repr(self.string)[1:-1]
        printer.print(f"sv.verbatim \"{string}\"")
        if self.operands:
            printer.print(" (")
            print_names(self.operands, printer)
            printer.print(") : ")
            print_types(self.operands, printer)


end_dialect()
