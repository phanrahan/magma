import magma as m
import magma.testing
import fault as f


def test_basic():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()

        with m.compile_guard("COND", defn_name="COND_compile_guard"):
            out = m.Register(m.Bit)()(io.I)

        io.O @= io.I

    m.compile("build/test_compile_guard_basic", _Top)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_basic.json",
        f"gold/test_compile_guard_basic.json")


def test_assert():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Valid[m.Bits[4]]), O=m.Out(m.Bits[4])) + m.ClockIO()
        io.O @= m.Register(m.Bits[4])()(io.I.data)

        with m.compile_guard("ASSERT_ON", "ASSERT_ON_compile_guard"):
            count = m.Register(m.UInt[2], has_enable=True)()
            count.I @= count.O + 1
            count.CE @= io.I.valid
            f.assert_immediate((count.O != 3) | (io.O.value() == 3))

    m.compile("build/test_compile_guard_assert", _Top, inline=True)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_assert.json",
        f"gold/test_compile_guard_assert.json")


def test_array():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bit]), O=m.Out(m.Bit)) + m.ClockIO()

        with m.compile_guard("COND", defn_name="COND_compile_guard"):
            out = m.Register(m.Bit)()(io.I[0])

        io.O @= io.I[1]

    m.compile("build/test_compile_guard_array", _Top)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_array.json",
        f"gold/test_compile_guard_array.json")


def test_multiple_array():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bit]), O=m.Out(m.Bit)) + m.ClockIO()

        with m.compile_guard("COND", defn_name="COND_compile_guard"):
            m.Register(m.Bit)()(io.I[1])
            m.Register(m.Bit)()(io.I[0])

        io.O @= io.I[1]

    m.compile("build/test_compile_guard_multiple_array", _Top)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_multiple_array.json",
        f"gold/test_compile_guard_multiple_array.json")


def test_nested_type():

    class _Top(m.Circuit):
        T = m.Product.from_fields("anon", dict(x=m.Bit, y=m.Bit))
        T = m.Array[2, T]

        io = m.IO(I=m.In(T), O=m.Out(m.Bit)) + m.ClockIO()

        with m.compile_guard("COND", defn_name="COND_compile_guard"):
            m.Register(m.Bit)()(io.I[1].x)
            m.Register(m.Bit)()(io.I[0].y)

        io.O @= io.I[0].x

    m.compile("build/test_compile_guard_nested_type", _Top)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_nested_type.json",
        f"gold/test_compile_guard_nested_type.json")
