import os
from typing import Dict

from magma.backend.coreir.insert_coreir_wires import insert_coreir_wires
from magma.backend.mlir.compile_to_mlir import compile_to_mlir
from magma.backend.mlir.compile_to_mlir_opts import CompileToMlirOpts
from magma.backend.mlir.mlir_to_verilog import (
    MlirToVerilogOpts,
    mlir_to_verilog,
)
from magma.circuit import DefineCircuitKind
from magma.common import slice_opts
from magma.compiler import Compiler
from magma.passes.clock import wire_clocks
from magma.passes.elaborate_tuples import elaborate_tuples
from magma.passes.finalize_whens import finalize_whens
from magma.passes.raise_logs_as_exceptions import raise_logs_as_exceptions_pass


class MlirCompiler(Compiler):
    def __init__(self, main: DefineCircuitKind, basename: str, opts: Dict):
        # TODO(rsetaluri): Make this a better error.
        assert "basename" not in opts
        opts["basename"] = basename
        self._compile_to_mlir_opts = slice_opts(
            opts, CompileToMlirOpts, keep=True
        )
        self._mlir_to_verilog_opts = slice_opts(
            opts, MlirToVerilogOpts, keep=True
        )
        super().__init__(main, basename, opts)

    def suffix(self):
        if self.opts.get("output_verilog", False):
            if self.opts.get("sv", False):
                return "sv"
            return "v"
        return "mlir"

    def run_pre_uniquification_passes(self):
        if self.opts.get("flatten_all_tuples", False):
            elaborate_tuples(self.main)
        # NOTE(leonardt): finalizing whens must happen after any
        # passes that modify the circuit.  This is because passes
        # could introduce more conditional logic, or they could
        # trigger elaboration on values used in existing coditiona
        # logic (which modifies the when builder)
        finalize_whens(self.main)

    def _run_passes(self):
        raise_logs_as_exceptions_pass(self.main)
        insert_coreir_wires(self.main, flatten=False)
        wire_clocks(self.main)

    def compile(self):
        self._run_passes()
        with open(f"{self.basename}.mlir", "w") as f:
            compile_to_mlir(
                self.main, sout=f, opts=self._compile_to_mlir_opts)
        if not self.opts.get("output_verilog", False):
            return
        outfile = (
            os.devnull
            if self.opts.get("split_verilog", False)
            else f"{self.basename}.{self.suffix()}"
        )
        with open(f"{self.basename}.mlir", "r") as fi:
            with open(outfile, "w") as fo:
                mlir_to_verilog(fi, fo, opts=self._mlir_to_verilog_opts)
