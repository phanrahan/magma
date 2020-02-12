from inspect import getouterframes, currentframe
from pathlib import PurePath
from .backend import verilog, blif, firrtl, dot, coreir_compiler
from .compiler import Compiler
from .config import get_compile_dir
from .uniquification import uniquification_pass, UniquificationMode

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
    basename = _get_basename(basename)
    opts = kwargs.copy()
    compiler = _make_compiler(output, main, basename, opts)

    # Default behavior is to perform uniquification, but can be overriden.
    uniquification_pass(main, opts.get("uniquify", "UNIQUIFY"))

    compiler.compile()

    if hasattr(main, "fpga"):
        main.fpga.constraints(basename)
