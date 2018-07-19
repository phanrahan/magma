import os
import inspect
import subprocess

from .passes import DefinitionPass
from .backend import verilog, blif, firrtl, dot
from .config import get_compile_dir
from .logging import error
from .circuit import isdefinition

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


def compile(basename, main, output='verilog', origin=None, include_coreir=False):
    check_definitions_are_unique(main)
    if get_compile_dir() == 'callee_file_dir':
        (_, filename, _, _, _, _) = inspect.getouterframes(inspect.currentframe())[1]
        file_path = os.path.dirname(filename)
        file_name = os.path.join(file_path, basename)
    else:
        file_name = basename

    if output == 'verilog':
        write_file(file_name, 'v', verilog.compile(main, include_coreir))
    elif output == 'blif':
        write_file(file_name, 'blif', blif.compile(main))
    elif output == 'firrtl':
        write_file(file_name, 'fir', firrtl.compile(main))
    elif output == 'coreir':
        # underscore so our coreir module doesn't conflict with coreir bindings
        # package
        from .backend import coreir_
        coreir_.compile(main, file_name + ".json")
    elif output == 'coreir-verilog':
        # underscore so our coreir module doesn't conflict with coreir bindings
        # package
        from .backend import coreir_
        coreir_.compile(main, file_name + ".json")
        subprocess.run(f"coreir -i {file_name}.json -o {file_name}.v", shell=True)
    elif output == 'dot':
        write_file(file_name, 'dot', dot.compile(main))

    if hasattr(main, 'fpga'):
        main.fpga.constraints(file_name);
