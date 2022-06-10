import io
import pytest

import magma as m
from magma.backend.mlir.mlir_to_verilog import (
    mlir_to_verilog,
    circt_opt_binary_exists,
    MlirToVerilogException,
)
from magma.testing.utils import with_config


def _skip_if_circt_opt_binary_does_not_exist():
    if not circt_opt_binary_exists():
        pytest.skip("no circt-opt binary found")


@with_config("circt_home", "/this_cant_be_a_real_directory/")
def test_no_binary():
    istream = io.TextIOWrapper(io.BytesIO())
    ostream = io.TextIOWrapper(io.BytesIO())

    with pytest.raises(FileNotFoundError):
        mlir_to_verilog(istream.buffer, ostream.buffer)


def test_basic():
    _skip_if_circt_opt_binary_does_not_exist()

    istream = io.TextIOWrapper(io.BytesIO())
    ostream = io.TextIOWrapper(io.BytesIO())

    mlir_to_verilog(istream.buffer, ostream.buffer)


def test_module():
    _skip_if_circt_opt_binary_does_not_exist()

    istream = io.TextIOWrapper(io.BytesIO())
    istream.write("module {}\n")
    istream.seek(0)
    ostream = io.TextIOWrapper(io.BytesIO())

    mlir_to_verilog(istream.buffer, ostream.buffer)

    ostream.seek(0)
    assert ostream.read() == ""


def test_bad_input():
    _skip_if_circt_opt_binary_does_not_exist()

    istream = io.TextIOWrapper(io.BytesIO())
    istream.write("blahblahblah")
    istream.seek(0)
    ostream = io.TextIOWrapper(io.BytesIO())

    with pytest.raises(MlirToVerilogException):
        mlir_to_verilog(istream.buffer, ostream.buffer)
