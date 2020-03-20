import itertools
import pytest
import magma as m
from magma.testing.utils import has_error


_DIGITAL_TYPES = [
    m.Bit,
    m.Clock,
    m.Reset,
    m.ResetN,
    m.AsyncReset,
    m.AsyncResetN,
    m.Enable
]


@pytest.mark.parametrize("in_type,out_type", itertools.product(_DIGITAL_TYPES,
                                                               _DIGITAL_TYPES))
def test_wire(caplog, in_type, out_type):
    i = m.In(in_type)()
    o = m.Out(out_type)()
    m.wire(i, o)
    wired = o.wired()
    if in_type is out_type:
        assert len(wired) == 1
        return
    assert len(wired) == 0
    msg = (f"Cannot wire {i.debug_name} (type={type(i)}) to {o} "
           f"(type={type(o)}) because {o.debug_name} is not a "
           f"{in_type}")
    assert has_error(caplog, msg)
