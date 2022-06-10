import io
import pytest
from typing import Optional

import magma as m
from magma.backend.mlir.mlir_to_verilog import (
    mlir_to_verilog,
    circt_opt_binary_exists,
    MlirToVerilogException,
)
from magma.testing.utils import with_config


_with_nonexistent_circt_home = with_config(
    "circt_home", "/this_isnt_a_real_directory/"
)


def _skip_if_circt_opt_binary_does_not_exist():
    if not circt_opt_binary_exists():
        pytest.skip("no circt-opt binary found")


def _run_test(input_: Optional[str] = None):
    istream = io.TextIOWrapper(io.BytesIO())
    ostream = io.TextIOWrapper(io.BytesIO())
    if input_ is not None:
        istream.write(input_)
        istream.seek(0)
    mlir_to_verilog(istream.buffer, ostream.buffer)
    return istream, ostream


def test_no_binary(_with_nonexistent_circt_home):
    with pytest.raises(FileNotFoundError):
        _run_test()


def test_basic():
    _skip_if_circt_opt_binary_does_not_exist()
    _, __ = _run_test()


def test_module():
    _skip_if_circt_opt_binary_does_not_exist()
    _, ostream = _run_test("module {}\n")
    ostream.seek(0)
    assert ostream.read() == ""


def test_bad_input():
    _skip_if_circt_opt_binary_does_not_exist()
    with pytest.raises(MlirToVerilogException):
        _run_test("blahblahblah")
