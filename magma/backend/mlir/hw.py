import dataclasses
from typing import Any, ClassVar, List, Mapping, Optional, Tuple

from magma.backend.mlir.common import default_field
from magma.backend.mlir.mlir import (
    begin_dialect,
    end_dialect,
    MlirAttribute,
    MlirDialect,
    MlirOp,
    MlirSymbol,
    MlirType,
    MlirValue,
)
from magma.backend.mlir.mlir_printer_utils import (
    print_attr_dict,
    print_names,
    print_signature,
    print_types,
)
from magma.backend.mlir.print_opts import PrintOpts
from magma.backend.mlir.printer_base import PrinterBase


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


@dataclasses.dataclass(frozen=True)
class InnerRefAttr(MlirAttribute):
    module: MlirSymbol
    name: MlirSymbol

    def emit(self) -> str:
        return f"#hw.innerNameRef<{self.module.name}::{self.name.name}>"


@dataclasses.dataclass(frozen=True)
class ParamDeclAttr(MlirAttribute):
    name: str
    type: MlirType
    value: Optional[MlirAttribute] = None

    def emit(self) -> str:
        s = f"{self.name}: {self.type.emit()}"
        if self.value is None:
            return s
        return f"{s} = {self.value.emit()}"


@dataclasses.dataclass(frozen=True)
class OutputFileAttr(MlirAttribute):
    filename: str
    exclude_from_file_list: bool = False
    include_replicated_ops: bool = False

    def emit(self) -> str:
        s = f"#hw.output_file<\"{self.filename}\""
        if self.exclude_from_file_list:
            s += f", excludeFromFileList"
        if self.include_replicated_ops:
            s += f", includeReplicatedOps"
        return f"{s}>"


@dataclasses.dataclass(frozen=True)
class FileListAttr(MlirAttribute):
    filename: str

    def emit(self) -> str:
        return f"#hw.output_filelist<\"{self.filename}\">"


@dataclasses.dataclass
class ModuleOpBase(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    name: MlirSymbol
    parameters: List[ParamDeclAttr] = default_field(list)

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        printer.print(f"hw.{self.op_name} {self.name.name}")
        if self.parameters:
            printer.print("<")
            printer.print(", ".join(param.emit() for param in self.parameters))
            printer.print(">")
        printer.print("(")
        print_signature(self.operands, printer, print_opts)
        printer.print(") -> (")
        print_signature(self.results, printer, print_opts, raw_names=True)
        printer.print(")")
        if self.attr_dict:
            printer.print(" attributes ")
            print_attr_dict(self.attr_dict, printer)


@dataclasses.dataclass
class ModuleOp(ModuleOpBase):
    op_name: ClassVar[str] = "module"

    def __post_init__(self):
        self._block = self.new_region().new_block()

    def add_operation(self, operation: MlirOp):
        self._block.add_operation(operation)


@dataclasses.dataclass
class ModuleExternOp(ModuleOpBase):
    op_name: ClassVar[str] = "module.extern"


@dataclasses.dataclass
class OutputOp(MlirOp):
    operands: List[MlirValue]

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        printer.print(f"hw.output ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands, printer)


@dataclasses.dataclass
class ConstantOp(MlirOp):
    results: List[MlirValue]
    value: int

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        print_names(self.results, printer)
        printer.print(f" = hw.constant {self.value} : ")
        print_types(self.results, printer)


@dataclasses.dataclass
class InstanceOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    name: str
    module: ModuleOpBase
    parameters: List[ParamDeclAttr] = default_field(list)
    sym: Optional[MlirSymbol] = None

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        if self.results:
            print_names(self.results, printer)
            printer.print(" = ")
        printer.print(f"hw.instance \"{self.name}\" ")
        if self.sym is not None:
            printer.print(f"sym {self.sym.name} ")
        printer.print(f"{self.module.name.name}")
        if self.parameters:
            printer.print("<")
            printer.print(", ".join(param.emit() for param in self.parameters))
            printer.print(">")
        printer.print("(")
        operands = [
            f"{m_operand.raw_name}: {operand.name}: {operand.type.emit()}"
            for operand, m_operand in zip(self.operands, self.module.operands)
        ]
        printer.print(", ".join(operands))
        printer.print(") -> (")
        results = [
            f"{m_result.raw_name}: {result.type.emit()}"
            for result, m_result in zip(self.results, self.module.results)
        ]
        printer.print(", ".join(results))
        printer.print(")")
        if self.attr_dict:
            printer.print(" ")
            print_attr_dict(self.attr_dict, printer)


@dataclasses.dataclass
class ArrayGetOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        print_names(self.results, printer)
        printer.print(" = hw.array_get ")
        print_names(self.operands[0], printer)
        printer.print("[")
        print_names(self.operands[1], printer)
        printer.print("] : ")
        print_types(self.operands, printer)


@dataclasses.dataclass
class ArraySliceOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        print_names(self.results, printer)
        printer.print(" = hw.array_slice ")
        print_names(self.operands[0], printer)
        printer.print("[")
        print_names(self.operands[1], printer)
        printer.print("] : (")
        print_types(self.operands[0], printer)
        printer.print(") -> ")
        print_types(self.results[0], printer)


@dataclasses.dataclass
class ArrayCreateOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        print_names(self.results, printer)
        printer.print(" = hw.array_create ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands[0], printer)


@dataclasses.dataclass
class ArrayConcatOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        print_names(self.results, printer)
        printer.print(" = hw.array_concat ")
        print_names(self.operands, printer)
        printer.print(" : ")
        print_types(self.operands, printer)


@dataclasses.dataclass
class StructExtractOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]
    field: str

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        print_names(self.results, printer)
        printer.print(" = hw.struct_extract ")
        print_names(self.operands, printer)
        printer.print(f"[\"{self.field}\"] : ")
        print_types(self.operands, printer)


@dataclasses.dataclass
class StructCreateOp(MlirOp):
    operands: List[MlirValue]
    results: List[MlirValue]

    def print_op(self, printer: PrinterBase, print_opts: PrintOpts):
        print_names(self.results, printer)
        printer.print(" = hw.struct_create (")
        print_names(self.operands, printer)
        printer.print(") : ")
        print_types(self.results, printer)


end_dialect()
