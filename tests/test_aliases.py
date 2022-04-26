import pytest

import magma as m


@pytest.mark.parametrize(
    "original,alias",
    [
        (m.Register, m.Reg),
    ]
)
def test_aliases(original, alias):
    assert alias is original


