from .utils import check_files_equal
from magma import compile

def compile_and_regress(callee_file, name, vendor, main, *largs, **kwargs):
    build = 'build/' + name
    gold = 'gold/' + name

    compile(build, main(*largs, **kwargs))
    assert check_files_equal(callee_file, build+'.v', gold+'.v')

    if vendor in ['altera', 'xilinx', 'lattice']:
        if vendor == 'altera' or vendor == 'xilinx':
            constraints = '.ucf'
        if vendor == 'lattice': 
            constraints = '.pcf'
        assert check_files_equal(callee_file,
            build+constraints, gold+constraints)
