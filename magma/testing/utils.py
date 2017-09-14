"""
Infrastructure for writing magma tests
"""
import filecmp
import os
import sys
import difflib

def check_files_equal(callee_file, file1, file2):
    """
    Check if file1 == file2 where file1 and file2 are in the same path as
    callee_file (typically __file__ for the script calling this function)
    """
    file_path = os.path.dirname(callee_file)
    file1 = os.path.join(file_path, file1)
    file2 = os.path.join(file_path, file2)
    result = filecmp.cmp(file1, file2, shallow=False)
    if not result:
        with open(file1, "r") as file1:
            with open(file2, "r") as file2:
                diff = difflib.unified_diff(
                    file1.readlines(),
                    file2.readlines(),
                    fromfile=file1,
                    tofile=file2,
                )
                for line in diff:
                    sys.stderr.write(line)
    return result
