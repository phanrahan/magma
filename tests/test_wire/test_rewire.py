import pytest

import magma as m
from magma.testing.utils import has_warning


@pytest.mark.parametrize("first,second", ((0, 0), (0, 1)))
def test_anonymous_bits_rewiring_warning(first, second, caplog):
    x = m.Bit(name="x")
    x @= first
    x = m.as_bits(x)
    x @= second
    assert has_warning(caplog)
