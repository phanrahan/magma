import io
import pytest

import magma as m
from magma.backend.mlir.mlir_to_verilog import mlir_to_verilog
from magma.testing.utils import with_config


@with_config("circt_home", "/this_cant_be_a_real_directory/")
def test_no_binary():
    istream = io.TextIOWrapper(io.BytesIO())
    ostream = io.TextIOWrapper(io.BytesIO())

    with pytest.raises(FileNotFoundError):
        mlir_to_verilog(istream.buffer, ostream.buffer)
