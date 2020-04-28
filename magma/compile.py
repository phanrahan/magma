from inspect import getouterframes, currentframe
from pathlib import PurePath
from .backend import verilog, blif, firrtl, dot, coreir_compiler
from .compiler import Compiler
from .config import get_compile_dir
from .uniquification import uniquification_pass, UniquificationMode
from .passes.clock import WireClockPass
from .passes.drive_undriven import DriveUndrivenPass
from .passes.terminate_unused import TerminateUnusedPass
from magma.bind import BindPass
from magma.inline_verilog import ProcessInlineVerilogPass

__all__ = ["compile"]


def _make_compiler(output, main, basename, opts):
    if output == "verilog":
        return verilog.VerilogCompiler(main, basename)
    if output == "blif":
        return blif.BlifCompiler(main, basename)
    if output == "firrtl":
        return firrtl.FirrtlCompiler(main, basename)
    if output == "dot":
        return dot.DotCompiler(main, basename)
    if output == "coreir":
        return coreir_compiler.CoreIRCompiler(main, basename, opts)
    if output == "coreir-verilog":
        opts["output_verilog"] = True
        return coreir_compiler.CoreIRCompiler(main, basename, opts)
    raise NotImplementedError(f"Backend '{output}' not supported")


def _get_basename(basename):
    if get_compile_dir() == "callee_file_dir":
        callee_filename = getouterframes(currentframe())[2][1]
        callee_dir = PurePath(callee_filename).parent
        return str(callee_dir.joinpath(basename))
    return basename


def compile(basename, main, output="coreir-verilog", **kwargs):
    if hasattr(main, "circuit_definition"):
        main = main.circuit_definition
    basename = _get_basename(basename)
    opts = kwargs.copy()
    compiler = _make_compiler(output, main, basename, opts)

    # Default behavior is to perform uniquification, but can be overriden.
    uniquification_pass(main, opts.get("uniquify", "UNIQUIFY"))

    # Steps to process inline verilog generation. Required to be run after uniquification.
    ProcessInlineVerilogPass(main).run()

    # Bind after uniquification so the bind logic works on unique modules
    BindPass(main, compile).run()

    if opts.get("drive_undriven", False):
        DriveUndrivenPass(main).run()
    if opts.get("terminate_unused", False):
        TerminateUnusedPass(main).run()

    compiler.compile()

    if hasattr(main, "fpga"):
        main.fpga.constraints(basename)
