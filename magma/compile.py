import sys
import os
import inspect
import subprocess

from .passes import DefinitionPass, InstanceGraphPass
from .backend import verilog, blif, firrtl, dot
from .config import get_compile_dir
from .logging import warning
from .uniquification import uniquification_pass, UniquificationMode
import magma as m


__all__ = ['compile']


def write_file(file_name, extension, code):
    with open("{}.{}".format(file_name, extension), 'w') as file:
        file.write(code)


class CheckAnyMantleCircuits(DefinitionPass):
    def __init__(self, main):
        super().__init__(main)
        self.has_mantle_circuit = False

    def __call__(self, definition):
        if definition.debug_info.module is not None and \
                definition.debug_info.module.__name__.split(".")[0] == "mantle":
            self.has_mantle_circuit = True

    def _run(self, definition):
        for instance in getattr(definition, "instances", []):
            instancedefinition = type(instance)
            self._run( instancedefinition )

        self(definition)

    def run(self):
        super().run()
        return self.has_mantle_circuit


def __compile_to_coreir(main, file_name, opts):
    # Underscore so our coreir module doesn't conflict with coreir bindings
    # package.
    from .backend import coreir_
    context = opts.get("context", None)
    backend = coreir_.CoreIRBackend(context)
    backend.compile(main)
    passes = opts.get("passes", [])
    if "markdirty" not in passes:
        passes.append("markdirty")
    namespaces = opts.get("namespaces", ["global"])
    backend.context.run_passes(passes, namespaces)

    backend.modules[main.coreir_name].save_to_file(file_name + ".json")
    if opts.get("output_verilog", False):
        deps = set()
        pass_ = InstanceGraphPass(main)
        pass_.run()
        for key, _ in pass_.tsortedgraph:
            if key.coreir_lib:
                deps.add(key.coreir_lib)
            elif hasattr(key, 'wrappedModule'):
                deps |= key.coreir_wrapped_modules_libs_used
        # TODO(rsetaluri): Expose compilation to verilog in pycoreir rather than
        # calling the binary from the command line.
        lib_arg = ""
        if deps:
            lib_arg = f"-l {','.join(deps)}"
        cmd = f"coreir {lib_arg} -i {file_name}.json"
        if opts.get("split", ""):
            split = opts["split"]
            cmd += f" -o \"{split}/*.v\" -s"
        else:
            cmd += f" -o {file_name}.v"
        if opts.get("inline", False):
            cmd += " --inline"
        if opts.get("verilator_debug", False):
            cmd += " --verilator_debug"
        subprocess.run(cmd, shell=True)


def compile(basename, main, output='verilog', **kwargs):
    opts = kwargs.copy()

    # If the output is verilog and the main circuit includes a mantle circuit
    # and we're using the coreir mantle target, use coreir to generate verilog
    # by setting the output to coreir-verilog
    has_mantle_circuit = CheckAnyMantleCircuits(main).run()
    if output == "verilog" and m.mantle_target == "coreir" and has_mantle_circuit:
        warning("`m.compile` called with `output == verilog` and"
                " `m.mantle_target == \"coreir\"` and mantle has been imported,"
                " When generating verilog from circuits from the \"coreir\""
                " mantle target, you should set `output=\"coreir-verilog\"`."
                " Doing this automatically.")
        output = 'coreir-verilog'

    # Rather than having separate logic for 'coreir-verilog' mode, we defer to
    # 'coreir' mode with the 'output_verilog' option set to True.
    if output == 'coreir-verilog':
        opts["output_verilog"] = True
        output = "coreir"

    # Allow the user to pass in a mode for uniquification. The input is expected
    # as a string and maps to the UniquificationMode enum.
    uniquification_mode_str = opts.get("uniquify", "UNIQUIFY")
    uniquification_mode = getattr(UniquificationMode, uniquification_mode_str,
                                  None)
    if uniquification_mode is None:
        raise ValueError(f"Invalid uniquification mode "
                         f"{uniquification_mode_str}")
    uniquification_pass(main, uniquification_mode)

    if get_compile_dir() == 'callee_file_dir':
        (_, filename, _, _, _, _) = inspect.getouterframes(inspect.currentframe())[1]
        file_path = os.path.dirname(filename)
        file_name = os.path.join(file_path, basename)
    else:
        file_name = basename

    if output == 'verilog':
        suffix = "v"
        # Handle the case when DefineFromVerilogFile is used with a system
        # verilog file
        if hasattr(main, "verilog_file_name") and \
                os.path.splitext(main.verilog_file_name)[-1] == ".sv":
            suffix = "sv"
        write_file(file_name, suffix, verilog.compile(main))
    elif output == 'blif':
        write_file(file_name, 'blif', blif.compile(main))
    elif output == 'firrtl':
        write_file(file_name, 'fir', firrtl.compile(main))
    elif output == 'coreir':
        __compile_to_coreir(main, file_name, opts)
    elif output == 'dot':
        write_file(file_name, 'dot', dot.compile(main))
    else:
        raise NotImplementedError(f"Backend '{output}' not supported")

    if hasattr(main, 'fpga'):
        main.fpga.constraints(file_name);
