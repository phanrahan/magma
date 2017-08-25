import os
import inspect
from .backend import verilog, blif, firrtl
from .error import warn
from .config import get_compile_dir
from .simulator_interactive_frontend import simulate

__all__ = ['compile']


def write_file(file_name, extension, code):
    with open("{}.{}".format(file_name, extension), 'w') as file:
        file.write(code)


def compile(basename, main, output='verilog', origin=None, include_coreir=False):
    if get_compile_dir() == 'callee_file_dir':
        (_, filename, _, _, _, _) = inspect.getouterframes(inspect.currentframe())[1]
        file_path = os.path.dirname(filename)
        file_name = os.path.join(file_path, basename)
    else:
        file_name = basename

    if output == '--simulate': #FIXME
        simulate(main)
        return

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

    if hasattr(main, 'fpga'):
        fpga = main.fpga
        vendor = os.getenv('MANTLE', 'lattice')
        if   vendor == 'altera':
            write_file(file_name, 'qsf', fpga.qsf(basename.split('/')[-1]))
        elif vendor == 'xilinx':
            write_file(file_name, 'ucf', fpga.ucf())
        elif vendor == 'lattice' or vendor == 'silego':
            write_file(file_name, 'pcf', fpga.pcf())
