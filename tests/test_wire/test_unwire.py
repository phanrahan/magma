import pytest
import logging

import magma as m


Ts = [m.Bit, m.Bits[4], m.Tuple[m.Bit, m.Bits[4]], m.Array[4, m.Bits[4]]]
funcs = [
    # With explicit arg
    lambda x, y: x.unwire(y), m.unwire,
    # With implicit default arg
    lambda x, y: x.unwire(), lambda x, y: m.unwire(x)
]


@pytest.mark.parametrize('T', Ts)
@pytest.mark.parametrize('func', funcs)
def test_unwire_with_arg(T, func, caplog):
    x, y, z = T(), T(), T()
    x @= y
    func(x, y)
    x @= z

    assert not any(record.level >= logging.WARNING
                   for record in caplog.records)
