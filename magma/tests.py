"""
Infrastructure for writing magma tests
"""
import pytest

@pytest.yield_fixture(autouse=True)
def magma_test():
    """
    Clear the circuit cache before running, allows name reuse across tests
    without collisions
    """
    import magma.circuit
    magma.circuit.__magma_clear_circuit_cache()
    import magma.config
    magma.config.set_compile_dir('callee_file_dir')

import filecmp
import os

def magma_check_files_equal(callee_file, file1, file2):
    """
    Check if file1 == file2 where file1 and file2 are in the same path as
    callee_file (presumably __file__ for the script calling this function)
    """
    file_path = os.path.dirname(callee_file)
    return filecmp.cmp(os.path.join(file_path, file1), 
                       os.path.join(file_path, file2), shallow=False)
