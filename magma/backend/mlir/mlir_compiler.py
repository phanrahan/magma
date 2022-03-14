import io
from typing import Dict

from magma.backend.coreir.insert_coreir_wires import insert_coreir_wires
from magma.backend.coreir.insert_wrap_casts import insert_wrap_casts
from magma.backend.mlir.compile_to_mlir import compile_to_mlir
from magma.circuit import DefineCircuitKind
from magma.compiler import Compiler
from magma.passes.clock import wire_clocks
from magma.passes.find_errors import find_errors_pass


class MlirCompiler(Compiler):
    def __init__(self, main: DefineCircuitKind, basename: str, opts: Dict):
        super().__init__(main, basename, opts)

    def suffix(self):
        return "mlir"

    def _run_passes(self):
        insert_coreir_wires(self.main)
        insert_wrap_casts(self.main)
        wire_clocks(self.main)
        find_errors_pass(self.main)

    def generate_code(self):
        self._run_passes()
        sout = io.StringIO()
        compile_to_mlir(self.main, sout=sout)
        return sout.getvalue()
