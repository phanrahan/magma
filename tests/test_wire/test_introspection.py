import pytest

import magma as m


def test_value_bits():
    T = m.Bits[5]
    x = m.Out(T)(name="x")
    y = m.In(T)(name="y")
    for i in range(T.N):
        y[i] @= x[T.N - i - 1]
    assert isinstance(y.value(), T)
