import magma as m
from magma.testing import check_files_equal

# Stub operators for test
m.BitType.__and__ = \
    lambda x, y: m.DeclareCircuit("and", "I0", m.In(m.Bit),
                                         "I1", m.In(m.Bit),
                                         "O", m.Out(m.Bit))()(x, y)
m.BitType.__or__ = \
    lambda x, y: m.DeclareCircuit("or", "I0", m.In(m.Bit),
                                        "I1", m.In(m.Bit),
                                        "O", m.Out(m.Bit))()(x, y)
m.BitType.__invert__ = \
    lambda x: m.DeclareCircuit("invert", "I", m.In(m.Bit),
                               "O", m.Out(m.Bit))()(x)


def test_new_style_simple_mux():
    class Test(m.Circuit):
        io = m.IO(
            S=m.In(m.Bit),
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            O=m.Out(m.Bit),
        )

        io.O <= (io.S & io.I1) | (~io.S & io.I0)
    print(repr(Test))
    assert repr(Test) == """\
Test = DefineCircuit("Test", "S", In(Bit), "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
or_inst0 = or()
and_inst0 = and()
and_inst1 = and()
invert_inst0 = invert()
wire(and_inst0.O, or_inst0.I0)
wire(and_inst1.O, or_inst0.I1)
wire(Test.S, and_inst0.I0)
wire(Test.I1, and_inst0.I1)
wire(invert_inst0.O, and_inst1.I0)
wire(Test.I0, and_inst1.I1)
wire(Test.S, invert_inst0.I)
wire(or_inst0.O, Test.O)
EndCircuit()\
"""

    m.compile('build/test_new_style_simple_mux', Test, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/test_new_style_simple_mux.v",
                             f"gold/test_new_style_simple_mux.v")


def test_new_style_nested():
    Top = m.DefineCircuit("Top", "S", m.In(m.Bit), "I0", m.In(m.Bit),
                          "I1", m.In(m.Bit), "O", m.Out(m.Bit),)

    # Begin definition of Mux while in the middle of defining Top.
    class Mux(m.Circuit):
        io = m.IO(
            S=m.In(m.Bit),
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            O=m.Out(m.Bit),
        )

        io.O <= (io.S & io.I1) | (~io.S & io.I0)

    # Continue defining Top.
    mux = Mux()
    mux.I0 <= Top.I0
    mux.I1 <= Top.I1
    mux.S <= Top.S
    Top.O <= mux.O
    m.EndDefine()

    assert repr(Mux) == """\
Mux = DefineCircuit("Mux", "S", In(Bit), "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
or_inst0 = or()
and_inst0 = and()
and_inst1 = and()
invert_inst0 = invert()
wire(and_inst0.O, or_inst0.I0)
wire(and_inst1.O, or_inst0.I1)
wire(Mux.S, and_inst0.I0)
wire(Mux.I1, and_inst0.I1)
wire(invert_inst0.O, and_inst1.I0)
wire(Mux.I0, and_inst1.I1)
wire(Mux.S, invert_inst0.I)
wire(or_inst0.O, Mux.O)
EndCircuit()\
"""
    assert repr(Top) == """\
Top = DefineCircuit("Top", "S", In(Bit), "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
Mux_inst0 = Mux()
wire(Top.S, Mux_inst0.S)
wire(Top.I0, Mux_inst0.I0)
wire(Top.I1, Mux_inst0.I1)
wire(Mux_inst0.O, Top.O)
EndCircuit()\
"""
