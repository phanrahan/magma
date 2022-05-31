import pytest

import magma as m
from magma.testing import check_files_equal


def test_when_with_default():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S):
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


def test_when_multiple_drivers():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]),
                  O0=m.Out(m.Bit), O1=m.Out(m.Bit))

        io.O0 @= io.I[1]
        io.O1 @= io.I[0]
        with m.when(io.S[0]) as c0:
            with m.when(io.S[1]) as c1:
                io.O0 @= io.I[0]
                io.O1 @= io.I[1]

    m.compile("build/test_when_multiple_drivers", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_multiple_drivers.v",
                             "gold/test_when_multiple_drivers.v")


def test_when_memory():
    class Foo(m.Circuit):
        io = m.IO(
            data0=m.In(m.Bits[8]), addr0=m.In(m.Bits[5]), en0=m.In(m.Bit),
            data1=m.In(m.Bits[8]), addr1=m.In(m.Bits[5]), en1=m.In(m.Bit),
            out=m.Out(m.Bits[8])
        )

        mem = m.Memory(32, m.Bits[8])()
        with m.when(io.en0):
            mem[io.addr0] @= io.data0
            io.out @= mem[io.addr0]
        with m.elsewhen(io.en1):
            mem[io.addr1] @= io.data1
            io.out @= mem[io.addr1]

    m.compile("build/test_when_memory", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_memory.v",
                             "gold/test_when_memory.v")


@pytest.mark.parametrize('T', [m.Array[2, m.Tuple[m.Bit, m.Bits[2]]],
                               m.Tuple[m.Bits[2], m.Bit]])
def test_when_nested(T):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, T]),
                  S=m.In(m.Bit),
                  O=m.Out(T))

        io.O @= io.I[1]
        with m.when(io.S):
            io.O @= io.I[0]

    T_str = str(T)\
        .replace('(', '')\
        .replace(')', '')\
        .replace('[', '')\
        .replace(']', '')\
        .replace(',', '')\
        .replace(' ', '')
    m.compile(f"build/test_when_nested_{T_str}", Foo, inline=True)
    assert check_files_equal(__file__,
                             f"build/test_when_nested_{T_str}.v",
                             f"gold/test_when_nested_{T_str}.v")
