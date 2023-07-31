import tempfile
import pytest

from hwtypes import BitVector
import fault as f

import magma as m
from magma.mantle import Decoder, decode


class DecodeFuncWrapper(m.Circuit):
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[2**8]))
    io.O @= decode(io.I)


@pytest.mark.parametrize("circ", [Decoder(8), DecodeFuncWrapper])
def test_decode_simple(circ):
    n = 8
    tester = f.Tester(circ)
    tester.circuit.I = I = BitVector.random(n)
    tester.eval()
    tester.circuit.O.expect(BitVector[2**n](1) << BitVector[2**n](int(I)))
    with tempfile.TemporaryDirectory() as tempdir:
        tester.compile_and_run("verilator", magma_output="mlir-verilog",
                               magma_opts={"check_circt_opt_version": False},
                               directory=tempdir)
