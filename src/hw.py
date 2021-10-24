import dataclasses
from typing import List, Tuple

from mlir import MlirDialect, begin_dialect, end_dialect
from mlir_printer_utils import print_names, print_types, print_signature
from mlir import MlirOp, MlirRegion, MlirBlock
from mlir import MlirValue
from mlir import MlirType
from printer_base import PrinterBase


hw = MlirDialect("hw")
begin_dialect(hw)


@dataclasses.dataclass(frozen=True)
class ArrayType(MlirType):
    dims: Tuple[int]
    T: MlirType

    def emit(self) -> str:
        dim_str = "x".join(map(str, self.dims))
        return f"!hw.array<{dim_str}x{self.T.emit()}>"


@dataclasses.dataclass(frozen=True)
class StructType(MlirType):
    fields: Tuple[Tuple[str, MlirType]]

    def emit(self) -> str:
        field_str = ", ".join(f"{k}: {t.emit()}" for k, t in self.fields)
        return f"!hw.struct<{field_str}>"


@dataclasses.dataclass(frozen=True)
class InOutType(MlirType):
    T: MlirType

    def emit(self) -> str:
        return f"!hw.inout<{self.T.emit()}>"


@dataclasses.dataclass
class ModuleOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    name: str

    def __post_init__(self):
        self.regions.append(MlirRegion())
        self.regions[0].blocks.append(MlirBlock())
        self._block = self.regions[0].blocks[0]        

    def print_op(self, printer: PrinterBase):
        printer.print(f"hw.module @{self.name}(")
        print_signature(self.operands, printer)
        printer.print(") -> (")
        print_signature(self.results, printer)
        printer.print(")")

    def add_operation(self, operation: MlirOp):
        self._block.operations.append(operation)


@dataclasses.dataclass
class OutputOp(MlirOp):
    operands: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        printer.print(f"hw.output ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands, printer)


@dataclasses.dataclass
class ConstantOp(MlirOp):
    results: List[MlirValue]
    value: int

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = hw.constant {self.value} : ")
        print_types(self.results, printer)


@dataclasses.dataclass
class ModuleExternOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    name: str

    def print_op(self, printer: PrinterBase):
        printer.print(f"hw.module.extern @{self.name}(")
        print_signature(self.operands, printer)
        printer.print(") -> (")
        print_signature(self.results, printer)
        printer.print(")")


@dataclasses.dataclass
class InstanceOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    name: str
    module: str

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(f" = hw.instance \"{self.name}\" ")
        printer.print(f"@{self.module}(")
        print_names(self.operands, printer)
        printer.print(") : (")
        print_types(self.operands, printer)
        printer.print(") -> (")
        print_types(self.results, printer)
        printer.print(")")


@dataclasses.dataclass
class ArrayGetOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(" = hw.array_get ")
        print_names(self.operands[0], printer)
        printer.print("[")
        print_names(self.operands[1], printer)
        printer.print("] : ")
        print_types(self.operands[0], printer)


@dataclasses.dataclass
class ArrayCreateOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(" = hw.array_create ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands[0], printer)


@dataclasses.dataclass
class StructExtractOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    field: str

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(" = hw.struct_extract ")
        print_names(self.operands, printer)
        printer.print(f"[\"{self.field}\"] : ")
        print_types(self.operands, printer)


@dataclasses.dataclass
class StructCreateOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase):
        print_names(self.results, printer)
        printer.print(" = hw.struct_create (")
        print_names(self.operands, printer)
        printer.print(") : ")
        print_types(self.results, printer)


end_dialect()
