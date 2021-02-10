from inspect import getouterframes, currentframe
from pathlib import PurePath

from magma.backend import verilog, blif, firrtl, dot, coreir_compiler
from magma.bind import BindPass
from magma.compiler import Compiler
from magma.config import get_compile_dir
from magma.inline_verilog import ProcessInlineVerilogPass
from magma.passes.black_box import BlackBoxPass
from magma.passes.stub import StubPass
from magma.passes.clock import WireClockPass
from magma.passes.drive_undriven import DriveUndrivenPass
from magma.passes.terminate_unused import TerminateUnusedPass
from magma.uniquification import uniquification_pass, UniquificationMode


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


def _run_if_in(dct, key, fn):
    try:
        value = dct[key]
    except KeyError:
        return
    fn(value)


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
    BindPass(main, compile, opts.get("user_namespace")).run()

    # Black box circuits if requested.
    _run_if_in(opts, "black_boxes", lambda bb: BlackBoxPass(main, bb).run())

    # Black box circuits if requested.
    _run_if_in(opts, "stubs", lambda stub: StubPass(main, stub).run())

    if opts.get("drive_undriven", False):
        DriveUndrivenPass(main).run()
    if opts.get("terminate_unused", False):
        TerminateUnusedPass(main).run()

    result = compiler.compile()
    result = {} if result is None else result

    if hasattr(main, "fpga"):
        main.fpga.constraints(basename)

    return result
