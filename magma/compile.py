import os
import inspect
from .backend import verilog, blif
from .config import get_compile_dir
from .simulator_interactive_frontend import simulate

__all__ = ['compile']

def compileqsf(basename, fpga):
    file = open(basename+'.qsf','w')
    name = basename.split('/')
    code = fpga.qsf(name[-1])
    file.write(code)
    file.close()

def compilepcf(basename, fpga):
    file = open(basename+'.pcf','w')
    code = fpga.pcf()
    file.write(code)
    file.close()

def compileucf(basename, fpga):
    file = open(basename+'.ucf','w')
    code = fpga.ucf()
    file.write(code)
    file.close()

def compileverilog(basename, main):
    file = open(basename+'.v','w')
    code = verilog.compile(main)
    file.write(code)
    file.close()
    #print('touch -m ' + basename + '.v')
    #os.system('touch -m ' + basename + '.v')

def compileblif(basename, main, origin):
    file = open(basename+'.blif','w')
    code = magma.blif.compile(main, origin)
    file.write(code)
    file.close()

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

    assert output in ['blif', 'verilog']
    if output == 'verilog':
        compileverilog(file_name, main)
    elif output == 'blif':
        compileblif(file_name, main, origin)

    if hasattr(main, 'fpga'):
        vendor = os.getenv('MANTLE', 'lattice')
        if   vendor == 'altera':
            compileqsf(file_name, main.fpga)
        elif vendor == 'xilinx':
            compileucf(file_name, main.fpga)
        elif vendor == 'lattice':
            compilepcf(file_name, main.fpga)
