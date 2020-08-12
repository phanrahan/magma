import pytest

import magma as m


def test_mux_of_ints():
    # We can't infer type of if all inputs are ints
    class Foo(m.Circuit):
        io = m.IO(S=m.In(m.Bit))
        with pytest.raises(TypeError) as e:
            m.mux([1, 2], io.S)
        assert str(e.value) == f"""\
Cannot use m.mux with non-magma types (need at least one to infer type)\
"""
