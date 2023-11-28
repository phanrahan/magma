import pytest

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

    m.compile("build/test_compile_guard_assert", _Top, output="mlir")
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_assert.mlir",
        f"gold/test_compile_guard_assert.mlir")


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


def test_anon_driver_driven():

    def make_top():

        class _Top(m.Circuit):
            io = m.IO(I=m.In(m.Bit))
            x = m.Bit()
            x @= io.I
            with m.compile_guard("COND", defn_name="A"):
                m.register(x)

        return _Top

    Top = make_top()
    basename = "test_compile_guard_anon_driver_driven"
    m.compile(f"build/{basename}", Top)
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.v", f"gold/{basename}.v"
    )


def test_anon_driver_undriven():

    def make_top():

        class _Top(m.Circuit):
            io = m.IO(I=m.In(m.Bit))
            x = m.Bit()
            with m.compile_guard("COND", defn_name="A"):
                m.register(x)

        return _Top

    Top = make_top()
    basename = "test_compile_guard_anon_driver_undriven"
    with pytest.raises(m.MagmaCompileException):
        m.compile(f"build/{basename}", Top)


def test_anon_driver_nested_type():

    def make_top():

        class _Top(m.Circuit):
            io = m.IO(I=m.In(m.Bit))
            T = m.Array[10, m.AnonProduct[{"x": m.Bits[10]}]]
            x = T()
            for x_i in x:
                for x_i_j in x_i.x:
                    x_i_j @= io.I
            with m.compile_guard("COND", defn_name="A"):
                m.register(x)

        return _Top

    Top = make_top()
    basename = "test_compile_guard_anon_driver_nested_type"
    m.compile(f"build/{basename}", Top)
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.v", f"gold/{basename}.v"
    )


@pytest.mark.skip(reason="nested compile guard context not yet implemented")
def test_nested_context():

    class _Top(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()

        with m.compile_guard("OUTER", defn_name="OUTER_compile_guard"):
            m.Register(m.Bit)()(io.I0)

            with m.compile_guard("INNER", defn_name="INNER_compile_guard"):
                m.Register(m.Bit)()(io.I1)

        io.O @= io.I0

    m.compile("build/test_compile_guard_nested_context", _Top)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_nested_context.json",
        f"gold/test_compile_guard_nested_context.json")


def test_basic_oldstyle():

    class _Top(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)] + m.ClockInterface()

        @classmethod
        def definition(io):
            with m.compile_guard("COND", defn_name="COND_compile_guard"):
                out = m.Register(m.Bit)()(io.I)

            io.O @= io.I

    m.compile("build/test_compile_guard_basic", _Top)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_basic.json",
        f"gold/test_compile_guard_basic.json")


def test_basic_undefined():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()

        with m.compile_guard("COND", defn_name="COND_compile_guard",
                             type='undefined'):
            out = m.Register(m.Bit)()(io.I)

        io.O @= io.I

    m.compile("build/test_compile_guard_basic_undefined", _Top)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_basic_undefined.json",
        f"gold/test_compile_guard_basic_undefined.json")


def test_vcc():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()

        with m.compile_guard("COND", defn_name="COND_compile_guard"):
            out = m.Register(m.Bit)()(io.I ^ 1)

        io.O @= io.I

    m.compile("build/test_compile_guard_basic_vcc", _Top)
    assert m.testing.check_files_equal(
        __file__, f"build/test_compile_guard_basic_vcc.json",
        f"gold/test_compile_guard_basic_vcc.json")


def test_drive_outputs():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()

        with pytest.raises(TypeError):
            with m.compile_guard("COND"):
                io.O @= m.Register(m.Bit)()(io.I ^ 1)


def test_anon_drivee():

    def make_top():
        class _Top(m.Circuit):
            io = m.IO(I=m.In(m.Bit))
            O = m.Bit()

            with m.compile_guard("COND"):
                O @= m.register(io.I)

        return _Top

    with pytest.raises(NotImplementedError):
        _ = make_top()


def test_compile_guard_select_basic():
    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()

        x = m.Register(m.Bit)()(io.I ^ 1)
        y = m.Register(m.Bit)()(io.I)

        io.O @= m.compile_guard_select(
            COND1=x, COND2=y, default=io.I
        )

    basename = "test_compile_guard_select_basic"
    m.compile(f"build/{basename}", _Top, inline=True)
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.v", f"gold/{basename}.v")


def test_compile_guard_select_complex_type():
    T = m.Product.from_fields("anonymous", dict(x=m.Bit, y=m.Bit))

    def make_top():

        class _Top(m.Circuit):
            io = m.IO(I0=m.In(T), I1=m.In(T), O=m.Out(T))
            io.O @= m.compile_guard_select(
                COND1=io.I0, COND2=io.I1, default=io.I0)

    with pytest.raises(TypeError):
        make_top()


def test_contained_inline_verilog():

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= io.I
        with m.compile_guard("DEBUG", "DebugModule"):
            reg = m.Register(m.Bit)(name="reg")
            reg.I @= reg.O | io.I
            m.inline_verilog("assert {io.I};")
            m.inline_verilog("assert ~{reg.O};")

    basename = "test_compile_guard_contained_inline_verilog"
    m.compile(f"build/{basename}", Top)
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.v", f"gold/{basename}.v")


def test_compile_guard_anon_driven_internal():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()

        with m.compile_guard("COND", defn_name="COND_compile_guard"):
            x = m.Bit(name="x")
            x.undriven()  # x is driven internally
            out = m.Register(m.Bit)()(x)

        io.O @= io.I

    basename = "test_compile_guard_anon_driven_internal"
    m.compile(f"build/{basename}", _Top, output="mlir")
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.mlir", f"gold/{basename}.mlir"
    )


def test_compile_guard_anon_driving_external():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()
        x = m.Bit(name="x")
        io.O @= x  # x drives an external value

        with pytest.raises(TypeError):
            with m.compile_guard("COND", defn_name="COND_compile_guard"):
                x @= m.Register(m.Bit)()(io.I)


def test_compile_guard_inline_verilog_reset():

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io += m.ClockIO(has_async_resetn=True)
        io.O @= io.I

        with m.compile_guard("COND", defn_name="COND_compile_guard"):
            m.inline_verilog(
                """
assert property (@(posedge {clk}) disable iff {rst} {x} |-> ##1 {x};
                """,
                x=io.I,
                rst=m.AsyncResetN(),
                clk=m.Clock()
            )

    basename = "test_compile_guard_inline_verilog_reset"
    m.compile(f"build/{basename}", _Top, output="mlir")
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.mlir", f"gold/{basename}.mlir")
