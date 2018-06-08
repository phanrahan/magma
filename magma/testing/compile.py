import os
from os.path import join
from .utils import check_files_equal
from magma import compile

BUILD = 'build'
GOLD = 'gold'

def compile_and_regress(callee_file, name, vendor, main, *largs, **kwargs):
    compile(join(BUILD,name), main(*largs, **kwargs), vendor=vendor)
    assert check_files_equal(callee_file, join(BUILD,name)+'.v', join(GOLD,name)+'.v')
    if vendor in ['altera', 'xilinx', 'lattice']:
        if vendor == 'altera' or vendor == 'xilinx':
            ucf = '.ucf'
        if vendor == 'lattice': 
            ucf = '.pcf'
        assert check_files_equal(callee_file, join(BUILD,name)+ucf, join(GOLD,name)+ucf)
