import pytest

import magma as m
from magma.testing import check_files_equal


def test_when_with_default():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S):
            print("Bar")
            io.O @= io.I[0]

    m.compile("build/test_when_with_default", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_with_default.v",
                             "gold/test_when_with_default.v")


def test_when_nested_with_default():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S[0]) as c0:
            with m.when(io.S[1]) as c1:
                io.O @= io.I[0]

    m.compile("build/test_when_nested_with_default", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_nested_with_default.v",
                             "gold/test_when_nested_with_default.v")


def test_when_override(caplog):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S):
            io.O @= io.I[0]
        io.O @= io.I[1]

    # TODO(when): Check warning
    m.compile("build/test_when_override", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_override.v",
                             "gold/test_when_override.v")

    expected = ("Wiring a previously conditionally wired value (Foo.O), "
                "existing conditional drivers will be discarded")
    assert str(caplog.records[0].msg) == expected


def test_when_else():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0]
        with m.otherwise():
            io.O @= io.I[1]

    m.compile("build/test_when_else", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_else.v",
                             "gold/test_when_else.v")


def test_when_elsewhen():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            io.O @= io.I[0]
        with m.elsewhen(io.S[1]):
            io.O @= io.I[1]
        with m.otherwise():
            io.O @= io.I[2]

    m.compile("build/test_when_elsewhen", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_elsewhen.v",
                             "gold/test_when_elsewhen.v")


def _check_err(value, name):
    expected = f"Cannot use {name} without a previous when"
    assert str(value) == expected


@pytest.mark.parametrize('fn,name', [
    (lambda x: m.elsewhen(x), 'elsewhen'),
    (lambda x: m.otherwise(), 'otherwise')])
def test_when_bad_syntax(fn, name):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with pytest.raises(SyntaxError) as e:
            # This should not have a _PREV_WHEN_COND to use
            with fn(io.S[1]):
                io.O @= io.I[1]
        _check_err(e.value, name)

        with m.when(io.S[0]):
            io.O @= io.I[0]

        # This when should clear _PREV_WHEN_COND
        with m.when(io.S[1]):
            # This should not have a _PREV_WHEN_COND to use
            with pytest.raises(SyntaxError) as e:
                with fn(io.S[1]):
                    io.O @= io.I[1]
            _check_err(e.value, name)


@pytest.mark.parametrize('fn,name', [
    (lambda x: m.elsewhen(x), 'elsewhen'),
    (lambda x: m.otherwise(), 'otherwise')])
def test_when_bad_otherwise(fn, name):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            io.O @= io.I[0]

        # This when should clear _PREV_WHEN_COND
        with m.otherwise():
            io.O @= io.I[1]

        # This should not have a _PREV_WHEN_COND to use
        with pytest.raises(SyntaxError) as e:
            with fn(io.S[1]):
                io.O @= io.I[1]
        _check_err(e.value, name)
