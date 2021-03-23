import magma as m
from magma.testing.utils import has_warning, magma_debug_section


def test_undirected_value_warning_1(caplog):
    with magma_debug_section():
        class Main(m.Circuit):
            io = m.IO(I=m.In(m.Bits[5]), O=m.Out(m.Bits[5]))
            x = m.Bits[5](name="x")
            y = m.Bits[5](name="y")
            x @= io.I
            # Backwards, should be wiring x to drive y
            # This produces a warning that you're overwriting the previous driver
            # of x
            m.wire(y, x)
            io.O @= y
    msg = """\
\033[1mtests/test_wire/test_undirected_error.py:15\033[0m: Wiring multiple outputs to same wire, using last connection. Input: x, Old Output: Main.I, New Output: y
>>             m.wire(y, x)\
"""
    assert has_warning(caplog, msg)


def test_undirected_value_error_2(caplog):
    with magma_debug_section():
        class Main(m.Circuit):
            io = m.IO(I=m.In(m.Bits[5]), O=m.Out(m.Bits[5]))
            x = m.Bits[5](name="x")
            y = m.Bits[5](name="y")
            # Backwards, should be wiring x to drive y
            m.wire(y, x)
            # This produces a warning that you're overwriting the previous driver
            # of x
            x @= io.I
            io.O @= y
    msg = """\
\033[1mtests/test_wire/test_undirected_error.py:34\033[0m: Wiring multiple outputs to same wire, using last connection. Input: x, Old Output: y, New Output: Main.I
>>             x @= io.I\
"""
    assert has_warning(caplog, msg)
