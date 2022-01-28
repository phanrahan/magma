import io
import sys
from typing import Optional

from magma.backend.mlir.printer_base import PrinterBase
from magma.backend.mlir.translation_unit import TranslationUnit
from magma.circuit import DefineCircuitKind


def compile_to_mlir(
        top: DefineCircuitKind, sout: Optional[io.TextIOBase] = None):
    if sout is None:
        sout = sys.stdout
    translation_unit = TranslationUnit(top)
    translation_unit.compile()
    printer = PrinterBase(sout=sout)
    hw_module_ops = translation_unit.mlir_module.block.operations
    for op in hw_module_ops:
        op.print(printer)
