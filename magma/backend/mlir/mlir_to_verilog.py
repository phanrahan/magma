import dataclasses
import io
from typing import Optional

import circt
import circt.passmanager

from magma.backend.mlir.errors import MlirCompilerError


@dataclasses.dataclass
class MlirToVerilogOpts:
    split_verilog: bool = False
    split_verilog_directory: Optional[str] = None


def mlir_to_verilog(
        istream: io.TextIOBase,
        ostream: io.TextIOBase,
        opts: MlirToVerilogOpts = MlirToVerilogOpts(),
):
    ir = istream.read()
    with circt.ir.Context() as ctx:
        circt.register_dialects(ctx)
        module = circt.ir.Module.parse(ir)
        passes = [
            "lower-seq-to-sv",
            "canonicalize",
            "hw.module(hw-cleanup)",
            "hw.module(prettify-verilog)",
        ]
        pass_string = ",".join(passes)
        pm = circt.passmanager.PassManager.parse(
            f"builtin.module({pass_string})"
        )
        pm.run(module.operation)
    if opts.split_verilog:
        directory = opts.split_verilog_directory or "."
        circt.export_split_verilog(module, directory)
    else:
        circt.export_verilog(module, ostream)
