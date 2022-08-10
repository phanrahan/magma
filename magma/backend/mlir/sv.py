import dataclasses
from typing import List, Optional

from magma.backend.mlir.hw import hw
from magma.backend.mlir.mlir import (
    MlirDialect, MlirOp, MlirBlock, MlirValue, MlirSymbol,
    begin_dialect, end_dialect)
from magma.backend.mlir.mlir_printer_utils import print_names, print_types
from magma.backend.mlir.printer_base import PrinterBase


sv = MlirDialect("sv")
begin_dialect(sv)


@dataclasses.dataclass
class RegOp(MlirOp):
    results: List[MlirValue]
    name: Optional[str] = None

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = sv.reg ")
        if self.name is not None:
            printer.print(f"{{name = \"{self.name}\"}} ")
        printer.print(": ")
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
class AssignBaseOp(MlirOp):
    operands: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        printer.print(f"sv.{self.op_name} ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands[1], printer)


@dataclasses.dataclass
class AssignOp(AssignBaseOp):
    operands: List[MlirValue]
    op_name = "assign"


@dataclasses.dataclass
class PAssignOp(AssignBaseOp):
    operands: List[MlirValue]
    op_name = "passign"


@dataclasses.dataclass
class BPAssignOp(AssignBaseOp):
    operands: List[MlirValue]
    op_name = "bpassign"


@dataclasses.dataclass
class AlwaysFFOp(MlirOp):
    operands: List[MlirValue]
    clock_edge: str
    reset_type: str = None
    reset_edge: str = None

    def __post_init__(self):
        self._body_block = self.new_region().new_block()
        if self.reset_type is None:
            return
        self._reset_block = self.new_region().new_block()

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
        raise NotImplementedError()


@dataclasses.dataclass
class AlwaysCombOp(MlirOp):
    def __post_init__(self):
        self._body_block = self.new_region().new_block()

    @property
    def body_block(self) -> MlirBlock:
        return self._body_block

    def print(self, printer: PrinterBase):
        printer.print("sv.alwayscomb {")
        printer.flush()
        printer.push()
        self.body_block.print(printer)
        printer.pop()
        printer.print_line("}")

    def print_op(self, printer: PrinterBase):
        raise NotImplementedError()


@dataclasses.dataclass
class InitialOp(MlirOp):
    def __post_init__(self):
        self._block = self.new_region().new_block()

    def add_operation(self, operation: MlirOp):
        self._block.add_operation(operation)

    def print_op(self, printer: PrinterBase):
        printer.print("sv.initial")


@dataclasses.dataclass
class WireOp(MlirOp):
    results: List[MlirValue]
    name: Optional[str] = None
    sym: Optional[MlirSymbol] = None

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(" = sv.wire ")
        if self.sym is not None:
            printer.print(f"sym {self.sym.name} ")
        if self.name is not None:
            printer.print(f"{{name=\"{self.name}\"}} ")
        printer.print(": ")
        print_types(self.results, printer)


def _esacpe_string(string: str):
    # NOTE(rsetaluri): This is a hack to "double-escape" escape characters like
    # `\n`, `\t`.
    return (
        repr(string)[1:-1]
        .replace("\"", "\\\"")
        .replace("\\\'", "'")
    )


@dataclasses.dataclass
class VerbatimOp(MlirOp):
    operands: List[MlirOp]
    string: str

    def print_op(self, printer: PrinterBase):
        string = _esacpe_string(self.string)
        printer.print(f"sv.verbatim \"{string}\"")
        if self.operands:
            printer.print(" (")
            print_names(self.operands, printer)
            printer.print(") : ")
            print_types(self.operands, printer)


@dataclasses.dataclass
class VerbatimExprOp(MlirOp):
    operands: List[MlirOp]
    results: List[MlirOp]
    expr: str

    def print_op(self, printer: PrinterBase):
        expr = _esacpe_string(self.expr)
        print_names(self.results, printer)
        printer.print(f" = sv.verbatim.expr \"{expr}\"")
        printer.print(" (")
        print_names(self.operands, printer)
        printer.print(") : (")
        print_types(self.operands, printer)
        printer.print(") -> (")
        print_types(self.results, printer)
        printer.print(")")


@dataclasses.dataclass
class BindOp(MlirOp):
    instance: hw.InnerRefAttr

    def print_op(self, printer: PrinterBase):
        printer.print(f"sv.bind {self.instance.emit()}")


@dataclasses.dataclass
class IfDefOp(MlirOp):
    cond: str

    def __post_init__(self):
        self._then_block = self.new_region().new_block()
        self._else_block = None

    @property
    def then_block(self) -> MlirBlock:
        return self._then_block

    @property
    def else_block(self) -> MlirBlock:
        if self._else_block is None:
            self._else_block = self.new_region().new_block()
        return self._else_block

    def print(self, printer: PrinterBase):
        printer.print(f"sv.ifdef \"{self.cond}\" {{")
        printer.flush()
        printer.push()
        self._then_block.print(printer)
        printer.pop()
        printer.print("}")
        if self._else_block is None:
            printer.flush()
            return
        printer.print(" else {")
        printer.flush()
        printer.push()
        self._else_block.print(printer)
        printer.pop()
        printer.print_line("}")

    def print_op(self, printer: PrinterBase):
        raise NotImplementedError()


@dataclasses.dataclass
class IfOp(MlirOp):
    operands: List[MlirOp]

    def __post_init__(self):
        self._then_block = self.new_region().new_block()
        self._else_block = None

    @property
    def then_block(self) -> MlirBlock:
        return self._then_block

    @property
    def else_block(self) -> MlirBlock:
        if self._else_block is None:
            self._else_block = self.new_region().new_block()
        return self._else_block

    def print(self, printer: PrinterBase):
        printer.print(f"sv.if ")
        print_names(self.operands[0], printer)
        printer.print(" {")
        printer.flush()
        printer.push()
        self._then_block.print(printer)
        printer.pop()
        printer.print("}")
        if self._else_block is None:
            printer.flush()
            return
        printer.print(" else {")
        printer.flush()
        printer.push()
        self._else_block.print(printer)
        printer.pop()
        printer.print_line("}")

    def print_op(self, printer: PrinterBase):
        raise NotImplementedError()


@dataclasses.dataclass
class XMROp(MlirOp):
    results: List[MlirOp]
    is_rooted: bool
    path: List[str]

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = sv.xmr ")
        if self.is_rooted:
            printer.print(f"isRooted ")
        path = [f"\"{p}\"" for p in self.path]
        path = f"{', '.join(path)}"
        printer.print(f"{path} : ")
        print_types(self.results, printer)


@dataclasses.dataclass
class ArrayIndexInOutOp(MlirOp):
    operands: List[MlirOp]
    results: List[MlirOp]

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = sv.array_index_inout ")
        print_names(self.operands[0], printer)
        printer.print("[")
        print_names(self.operands[1], printer)
        printer.print("] : ")
        print_types(self.operands, printer)


end_dialect()
