"""
Infrastructure for writing magma tests
"""
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

check_files_equal = magma_check_files_equal
