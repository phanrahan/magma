"""
Infrastructure for writing magma tests
"""
import difflib
import filecmp
import os
import pytest
import shutil
import sys

from typing import Optional

from magma.config import get_debug_mode, set_debug_mode, config
from magma.conversions import bits
from magma.protocol_type import MagmaProtocolMeta, MagmaProtocol
from magma.t import Type, Direction


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


def has_debug(caplog, msg=None):
    return has_log(caplog, "DEBUG", msg)


def has_info(caplog, msg=None):
    return has_log(caplog, "INFO", msg)


def has_error(caplog, msg=None):
    return has_log(caplog, "ERROR", msg)


def has_warning(caplog, msg=None):
    return has_log(caplog, "WARNING", msg)


class SimpleMagmaProtocolMeta(MagmaProtocolMeta):
    _CACHE = {}

    def _to_magma_(cls):
        return cls.T

    def _qualify_magma_(cls, direction: Direction):
        return cls[cls.T.qualify(direction)]

    def _flip_magma_(cls):
        return cls[cls.T.flip()]

    def _from_magma_value_(cls, val: Type):
        return cls(val)

    def __getitem__(cls, T):
        try:
            base = cls.base
        except AttributeError:
            base = cls
        dct = {"T": T, "base": base}
        derived = type(cls)(f"{base.__name__}[{T}]", (cls,), dct)
        return SimpleMagmaProtocolMeta._CACHE.setdefault(T, derived)

    def __repr__(cls):
        return str(cls)

    def __str__(cls):
        return cls.__name__


class SimpleMagmaProtocol(MagmaProtocol, metaclass=SimpleMagmaProtocolMeta):
    def __init__(self, val: Optional[Type] = None):
        if val is None:
            val = self.T()
        self._val = val

    def _get_magma_value_(self):
        return self._val

    def non_standard_operation(self):
        v0 = self._val << 2
        v1 = bits(self._val[0], len(self.T)) << 1
        return SimpleMagmaProtocol(v0 | v1 | bits(self._val[0], len(self.T)))


def with_config(key, value):

    def fixture():
        prev_value = getattr(config, key)
        setattr(config, key, value)
        yield
        setattr(config, key, prev_value)

    return pytest.fixture(fixture)


def check_gold(callee_file, filename):
    try:
        return check_files_equal(callee_file,
                                 f"build/{filename}",
                                 f"gold/{filename}")
    except FileNotFoundError:
        return False


def update_gold(callee_file, filename):
    file_path = os.path.dirname(callee_file)
    return shutil.copy(f"{file_path}/build/{filename}",
                       f"{file_path}/gold/{filename}")
