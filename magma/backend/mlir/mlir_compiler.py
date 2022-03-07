import io
from typing import Dict

from magma.backend.mlir.compile_to_mlir import compile_to_mlir
from magma.circuit import DefineCircuitKind
from magma.compiler import Compiler


class MlirCompiler(Compiler):
    def __init__(self, main: DefineCircuitKind, basename: str, opts: Dict):
        super().__init__(main, basename, opts)

    def suffix(self):
        return "mlir"

    def generate_code(self):
        sout = io.StringIO()
        compile_to_mlir(self.main, sout=sout)
        return sout.getvalue()
