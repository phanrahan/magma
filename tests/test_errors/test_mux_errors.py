import pytest

import magma as m


def test_mux_of_ints():
    # We can't infer type of if all inputs are ints
    class Foo(m.Circuit):
        io = m.IO(S=m.In(m.Bit))
        with pytest.raises(TypeError) as e:
            m.mux([1, 2], io.S)
        assert str(e.value) == f"""\
Could not infer mux type from [1, 2]
Need at least one magma value, BitVector, bool or tuple\
"""


def test_mux_of_mismatch_widths():
    # We can't infer type of if all inputs are ints
    class Foo(m.Circuit):
        io = m.IO(I0=m.In(m.Bits[2]), I1=m.In(m.Bits[3]), S=m.In(m.Bit))
        with pytest.raises(TypeError) as e:
            m.mux([io.I0, io.I1], io.S)
        assert str(e.value) == f"""\
Found incompatible types Bits[3] and Bits[2] in mux inference\
"""
