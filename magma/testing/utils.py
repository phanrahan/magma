"""
Infrastructure for writing magma tests
"""
import filecmp
import os
import sys
import difflib
from ..config import get_debug_mode, set_debug_mode


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


class _MagmaDebugSection:
    def __init__(self):
        self.__restore = get_debug_mode()

    def __enter__(self):
        set_debug_mode(True)

    def __exit__(self, typ, value, traceback):
        set_debug_mode(self.__restore)


def magma_debug_section():
    return _MagmaDebugSection()


def has_log(caplog, level=None, msg=None):
    if level is None and msg is None:
        return len(caplog.records) > 0
    if level and not msg:
        gen = (log.levelname == level for log in caplog.records)
    elif msg and not level:
        gen = (str(log.msg) == str(msg) for log in caplog.records)
    else:
        gen = (log.levelname == level and str(log.msg) == str(msg)
               for log in caplog.records)
    return any(gen)


def has_error(caplog, msg=None):
    return has_log(caplog, "ERROR", msg)


def has_warning(caplog, msg=None):
    return has_log(caplog, "WARNING", msg)
