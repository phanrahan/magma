import io
from typing import Dict

from magma.backend.coreir.insert_coreir_wires import insert_coreir_wires
from magma.backend.coreir.insert_wrap_casts import insert_wrap_casts
from magma.backend.mlir.compile_to_mlir import compile_to_mlir
from magma.backend.mlir.compile_to_mlir_opts import CompileToMlirOpts
from magma.backend.mlir.mlir_to_verilog import mlir_to_verilog
from magma.circuit import DefineCircuitKind
from magma.common import slice_opts
from magma.compiler import Compiler
from magma.passes.clock import wire_clocks
from magma.passes.find_errors import find_errors_pass


class MlirCompiler(Compiler):
    def __init__(self, main: DefineCircuitKind, basename: str, opts: Dict):
        self._compile_to_mlir_opts = slice_opts(opts, CompileToMlirOpts)
        super().__init__(main, basename, opts)

    def suffix(self):
        if self.opts.get("output_verilog", False):
            if self.opts.get("sv", False):
                return "sv"
            return "v"
        return "mlir"

    def _run_passes(self):
        insert_coreir_wires(self.main)
        insert_wrap_casts(self.main)
        wire_clocks(self.main)
        find_errors_pass(self.main)

    def compile(self):
        self._run_passes()
        with open(f"{self.basename}.mlir", "w") as f:
            compile_to_mlir(
                self.main, sout=f, opts=self._compile_to_mlir_opts)
        if not self.opts.get("output_verilog", False):
            return
        with open(f"{self.basename}.mlir", "rb") as fi:
            with open(f"{self.basename}.{self.suffix()}", "wb") as fo:
                mlir_to_verilog(fi, fo)
