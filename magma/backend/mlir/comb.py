import dataclasses
from typing import List

from magma.backend.mlir.mlir import MlirDialect, begin_dialect, end_dialect
from magma.backend.mlir.mlir_printer_utils import print_names, print_types
from magma.backend.mlir.mlir import MlirValue, MlirOp
from magma.backend.mlir.printer_base import PrinterBase


comb = MlirDialect("comb")
begin_dialect(comb)


@dataclasses.dataclass
class BaseOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    op_name: str

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = comb.{self.op_name} ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.results, printer)


@dataclasses.dataclass
class ConcatOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = comb.concat ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands, printer)


@dataclasses.dataclass
class ExtractOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    lo: int

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(" = comb.extract ")
        print_names(self.operands, printer)
        printer.print(f" from {self.lo} : (")
        print_types(self.operands, printer)
        printer.print(") -> ")
        print_types(self.results, printer)


@dataclasses.dataclass
class ICmpOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    predicate: str

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = comb.icmp {self.predicate} ")
        print_names(self.operands, printer)
        printer.print(f" : ")
        print_types(self.operands[0], printer)


@dataclasses.dataclass
class ParityOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = comb.parity ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands, printer)


end_dialect()
