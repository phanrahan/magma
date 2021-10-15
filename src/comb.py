import dataclasses
from typing import List

from mlir import MlirDialect, begin_dialect, end_dialect
from mlir_printer_utils import print_names, print_types
from mlir import MlirOp
from mlir import MlirValue
from printer_base import PrinterBase


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
        printer.print(" : (")
        print_types(self.operands, printer)
        printer.print(") -> (")
        print_types(self.results, printer)
        printer.print(")")


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


end_dialect()
