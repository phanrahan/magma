import magma as m
from magma.testing import check_files_equal


def test_inline_comb_basic():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bit), invert=m.In(m.Bit), O=m.Out(m.Bit))
        io += m.ClockIO()
        reg = m.Register(m.Bit)()

        @m.inline_combinational(debug=True, file_name="inline_comb.py")
        def logic():
            if io.invert:
                reg.I = ~reg.O
            else:
                reg.I = reg.O

        io.O @= reg.O

    m.compile("build/test_inline_comb_basic", Main, inline=True)
    assert check_files_equal(__file__, f"build/test_inline_comb_basic.v",
                             f"gold/test_inline_comb_basic.v")
