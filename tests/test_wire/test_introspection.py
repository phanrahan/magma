import magma as m
import pytest


@pytest.mark.parametrize("T", (m.Bits,))
def test_value_arr_type(T):
    class Foo(m.Circuit):
        x = m.Out(T[5])(name="x")
        y = m.In(T[5])(name="y")
        for i in range(5):
            y[i] @= x[4-i]
        assert isinstance(y.value(), T)
