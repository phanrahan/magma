import sys
import os
import inspect
import subprocess

from .passes import DefinitionPass
from .backend import verilog, blif, firrtl, dot
from .config import get_compile_dir
from .logging import error
from .is_definition import isdefinition
from .logging import warning
import magma as m

__all__ = ['compile']


def write_file(file_name, extension, code):
    with open("{}.{}".format(file_name, extension), 'w') as file:
        file.write(code)


class MultipleDefinitionException(Exception):
    pass


class CheckDefinitionUniquenessPass(DefinitionPass):
    def __init__(self, main):
        super(CheckDefinitionUniquenessPass, self).__init__(main)
        self.seen = {}

    def __call__(self, definition):
        if definition.name not in self.seen:
            self.seen[definition.name] = set()
        self.seen[definition.name].add(definition)

    def _run(self, definition):
        if not isdefinition(definition):
            return

        for instance in definition.instances:
            instancedefinition = type(instance)
            if isdefinition(instancedefinition):
                self._run( instancedefinition )

        self(definition)

    def run(self):
        super(CheckDefinitionUniquenessPass, self).run()
        duplicated = []
        #print(self.seen)
        for name, definitions in self.seen.items():
            if len(definitions) > 1:
                duplicated.append((name, definitions))
                error("Found multiple definitions for {}".format(name))

        if len(duplicated):
            raise MultipleDefinitionException([name for name, _ in duplicated])


def check_definitions_are_unique(circuit):
    CheckDefinitionUniquenessPass(circuit).run()


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
    backend = coreir_.CoreIRBackend()
    backend.compile(main)
    if opts.get("passes", False):
        backend.context.run_passes(opts["passes"], ["global"])

    backend.modules[main.coreir_name].save_to_file(file_name + ".json")
    if opts.get("output_verilog", False):
        # TODO(rsetaluri): Expose compilation to verilog in pycoreir rather than
        # calling the binary from the command line.
        lib_arg = ""
        if backend.libs_used:
            lib_arg = f"-l {','.join(backend.libs_used)}"
        cmd = f"coreir {lib_arg} -i {file_name}.json"
        if opts.get("split", ""):
            split = opts["split"]
            cmd += f" -o \"{split}/*.v\" -s"
        else:
            cmd += f" -o {file_name}.v"
        if opts.get("inline", False):
            cmd += " --inline"
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

    check_definitions_are_unique(main)
    if get_compile_dir() == 'callee_file_dir':
        (_, filename, _, _, _, _) = inspect.getouterframes(inspect.currentframe())[1]
        file_path = os.path.dirname(filename)
        file_name = os.path.join(file_path, basename)
    else:
        file_name = basename

    if output == 'verilog':
        write_file(file_name, 'v', verilog.compile(main))
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
