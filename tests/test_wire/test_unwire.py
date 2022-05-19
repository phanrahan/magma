import pytest
import logging

import magma as m
from magma.testing.utils import has_warning


Ts = [m.Bit, m.Bits[4], m.Tuple[m.Bit, m.Bits[4]], m.Array[4, m.Bits[4]]]
funcs = [
    # With explicit arg
    lambda x, y: x.unwire(y), m.unwire,
    # With implicit default arg
    lambda x, y: x.unwire(), lambda x, y: m.unwire(x)
]


@pytest.mark.parametrize('T', Ts)
@pytest.mark.parametrize('func', funcs)
def test_unwire_basic(T, func, caplog):
    x, y, z = T(), T(), T()
    x @= y
    func(x, y)
    x @= z

    assert not any(record.level >= logging.WARNING
                   for record in caplog.records)


@pytest.mark.parametrize('T', Ts)
@pytest.mark.parametrize('func', funcs[2:4])
def test_unwire_undriven(T, func, caplog):
    m.config.set_debug_mode(True)
    x, y = T(name="Foo"), T()
    func(x, y)
    m.config.set_debug_mode(False)

    def make_expcted_log(value_str):
        return f"""\
\033[1mtests/test_wire/test_unwire.py:13\033[0m: Unwire called on undriven value {value_str}, ignoring
>>     lambda x, y: x.unwire(), lambda x, y: m.unwire(x)\
"""  # noqa

    assert has_warning(caplog, make_expcted_log("Foo"))
