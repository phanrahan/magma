import os

import pytest

import fault
import magma as m


def test_bit_pattern_simple():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bit))
        bit_pat = m.BitPattern("b??1??01?")
        io.O @= bit_pat == io.I

    m.compile("build/Foo", Foo)

    tester = fault.Tester(Foo)
    tester.circuit.I = 0b00100010
    tester.eval()
    tester.circuit.O.expect(1)
    tester.circuit.I = 0b10100010
    tester.eval()
    tester.circuit.O.expect(1)
    tester.circuit.I = 0b10100000
    tester.eval()
    tester.circuit.O.expect(0)
    tester.compile_and_run("verilator",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_as_bv():
    x = m.BitPattern("b1001")
    assert x.as_bv() == 0b1001

    y = m.BitPattern("b1??1")
    with pytest.raises(TypeError) as e:
        y.as_bv()
    assert (str(e.value) ==
            "Can only convert BitPattern with no don't cares to int")


def test_hashable():
    x = m.BitPattern("b10?1")
    y = m.BitPattern("b1?10")
    dict_ = {
        x: 1,
        y: 0
    }
    assert dict_[x] == 1
    assert dict_[y] == 0
