import pytest

import magma as m
from magma.testing.utils import has_warning, has_error


@pytest.mark.parametrize("first,second", ((0, 0), (0, 1)))
def test_anonymous_bits_rewiring_warning(first, second, caplog):
    x = m.Bit(name="x")
    x @= first
    x = m.as_bits(x)
    x @= second
    assert has_warning(caplog)


@pytest.fixture
def _setup_and_teardown():
    prev = m.config.config.rewire_log_level
    m.config.config.rewire_log_level = "ERROR"
    yield
    m.config.config.rewire_log_level = prev


# TODO(leonardt): use magma.testing.utils.with_config once #1090 is merged
def test_rewire_error(caplog, _setup_and_teardown):
    x = m.Bit(name="x")
    x @= 0
    x @= 1
    assert has_error(caplog)

    # NOTE(leonardt): We additionally check that compiling a circuit with a
    # rewiring error causes an exception (just a double-check since this
    # functionality is independent of the type of error logged).
    class Foo(m.Circuit):
        io = m.IO(O=m.Out(m.Bit))
        io.O @= 0
        io.O @= 1

    with pytest.raises(m.compile_exception.MagmaCompileException):
        m.compile("build/Foo", Foo)
