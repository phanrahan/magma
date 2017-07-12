import os
import inspect
from .backend import verilog, blif, firrtl
from .config import get_compile_dir
from .simulator_interactive_frontend import simulate

__all__ = ['compile']


def compile(basename, main, output='verilog', origin=None):
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
        code = verilog.compile(main)
        extension = 'v'
    elif output == 'blif':
        code = blif.compile(main, origin)
        extension = 'blif'
    elif output == 'firrtl':
        code = firrtl.compile(main)
    elif hasattr(main, 'fpga'):
        vendor = os.getenv('MANTLE', 'lattice')
        if   vendor == 'altera':
            code = fpga.qsf(basename.split('/')[-1])
            extension = "qsf"
        elif vendor == 'xilinx':
            code = fpga.ucf()
            extension = "ucf"
        elif vendor == 'lattice' or vendor == 'silego':
            code = fpga.pcf()
            extension = "pcf"
    else:
        raise NotImplementedError()

    with open("{}.{}".format(file_name, extension), 'w') as file:
        file.write(code)
