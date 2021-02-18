import magma as m
import magma.testing
import fault as f


def test_compile_guard_counter():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Valid[m.Bits[4]]), O=m.Out(m.Bits[4])) + m.ClockIO()
        io.O @= m.Register(m.Bits[4])()(io.I.data)

        with m.compile_guard("ASSERT_ON"):
            count = m.Register(m.UInt[2], has_enable=True)()
            count.I @= count.O + 1
            count.CE @= io.I.valid
            f.assert_immediate((count.O != 3) | (io.O.value() == 3))

    m.compile("build/test_compile_guard_counter", Foo, inline=True)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_counter.v",
        f"gold/test_compile_guard_counter.v")
