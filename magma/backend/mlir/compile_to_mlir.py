import io
import sys
from typing import Optional

from magma.backend.mlir.compile_to_mlir_opts import CompileToMlirOpts
from magma.backend.mlir.print_opts import PrintOpts
from magma.backend.mlir.printer_base import PrinterBase
from magma.backend.mlir.translation_unit import TranslationUnit
from magma.circuit import DefineCircuitKind


def _make_print_opts(opts: CompileToMlirOpts) -> PrintOpts:
    print_locations = opts.location_info_style != "none"
    return PrintOpts(print_locations=print_locations)


def compile_to_mlir(
        top: DefineCircuitKind,
        sout: Optional[io.TextIOBase] = None,
        opts: CompileToMlirOpts = CompileToMlirOpts()):
    if sout is None:
        sout = sys.stdout
    translation_unit = TranslationUnit(top, opts)
    translation_unit.compile()
    printer = PrinterBase(sout=sout)
    translation_unit.mlir_module.print(printer, _make_print_opts(opts))
