"""
Infrastructure for writing magma tests
"""
import filecmp
import os
import sys
import difflib


def check_files_equal(callee_file, file1_name, file2_name):
    """
    Check if file1 == file2 where file1 and file2 are in the same path as
    callee_file (typically __file__ for the script calling this function)
    """
    file_path = os.path.dirname(callee_file)
    file1_path = os.path.join(file_path, file1_name)
    file2_path = os.path.join(file_path, file2_name)
    print(file1_path, file2_path)
    result = filecmp.cmp(file1_path, file2_path, shallow=False)
    if not result:
        with open(file1_path, "r") as file1:
            with open(file2_path, "r") as file2:
                diff = difflib.unified_diff(
                    file2.readlines(),
                    file1.readlines(),
                    fromfile=file2_name,
                    tofile=file1_name,
                )
                for line in diff:
                    sys.stderr.write(line)
    return result
