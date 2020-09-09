import os
import fault
from hwtypes import BitVector, Bit
import magma as m
from magma.testing import check_files_equal


def test_inline_comb_basic():
    class Main(m.Circuit):
        io = m.IO(invert=m.In(m.Bit), O0=m.Out(m.Bit), O1=m.Out(m.Bit))
        io += m.ClockIO()
        reg = m.Register(m.Bit)()

        @m.inline_combinational(debug=True, file_name="inline_comb.py")
        def logic():
            if io.invert:
                reg.I @= ~reg.O
                O1 = ~reg.O
            else:
                reg.I @= reg.O
                O1 = reg.O

        io.O0 @= reg.O
        io.O1 @= O1

    m.compile("build/test_inline_comb_basic", Main, inline=True)
    assert check_files_equal(__file__, f"build/test_inline_comb_basic.v",
                             f"gold/test_inline_comb_basic.v")


def test_inline_comb_wire():
    import magma as magma_test

    class Main(magma_test.Circuit):
        io = magma_test.IO(invert=magma_test.In(magma_test.Bit), O=magma_test.Out(magma_test.Bit))
        io += magma_test.ClockIO()
        reg = magma_test.Register(magma_test.Bit)()

        @magma_test.inline_combinational(debug=True, file_name="test_inline_comb_wire.py")
        def logic():
            if io.invert:
                magma_test.wire(~reg.O, reg.I)
            else:
                magma_test.wire(reg.O, reg.I)

        io.O @= reg.O

    magma_test.compile("build/test_inline_comb_wire", Main, inline=True)
    assert check_files_equal(__file__, f"build/test_inline_comb_wire.v",
                             f"gold/test_inline_comb_wire.v")


def test_inline_comb_list():
    class Main(m.Circuit):
        io = m.IO(s=m.In(m.Bit), O0=m.Out(m.Bit), O1=m.Out(m.Bit))
        io += m.ClockIO()
        reg = m.Register(m.Bit)()

        @m.inline_combinational(debug=True, file_name="inline_comb.py")
        def logic():
            if io.s:
                O = [~reg.O, reg.O]
            else:
                O = [reg.O, ~reg.O]
        reg.I @= O[0]

        io.O0 @= O[0]
        io.O1 @= O[1]

    m.compile("build/test_inline_comb_list", Main, inline=True)
    assert check_files_equal(__file__, f"build/test_inline_comb_list.v",
                             f"gold/test_inline_comb_list.v")


def test_inline_comb_bv_bit_bool():
    class Main(m.Circuit):
        io = m.IO(s=m.In(m.Bit), O0=m.Out(m.Bits[2]), O1=m.Out(m.Bit),
                  O2=m.Out(m.Bit))

        @m.inline_combinational(debug=True, file_name="inline_comb.py")
        def logic():
            if io.s:
                x = [BitVector[2](2), Bit(1), True]
            else:
                x = [BitVector[2](1), Bit(0), False]

        io.O0 @= x[0]
        io.O1 @= x[1]
        io.O2 @= x[2]

    m.compile("build/test_inline_comb_bv_bit_bool", Main, inline=True)
    assert check_files_equal(__file__, f"build/test_inline_comb_bv_bit_bool.v",
                             f"gold/test_inline_comb_bv_bit_bool.v")


def test_Bit_bool():
    class test_Bit_bool(m.Circuit):
        io = m.IO(I=m.In(m.Bit), S=m.In(m.Bit), O0=m.Out(m.Bit),
                  O1=m.Out(m.Bit), O2=m.Out(m.Bit), O3=m.Out(m.Bit))
        @m.inline_combinational()
        def logic():
            if io.S:
                io.O0 @= io.I
                io.O1 @= io.I
                io.O2 @= False
                io.O3 @= Bit(False)
            else:
                io.O0 @= False
                io.O1 @= Bit(False)
                io.O2 @= io.I
                io.O3 @= io.I


    m.compile("build/test_Bit_bool", test_Bit_bool)

    tester = fault.Tester(test_Bit_bool)
    tester.circuit.S = 1
    tester.circuit.I = 0
    tester.eval()
    tester.circuit.O0.expect(0)
    tester.circuit.O1.expect(0)
    tester.circuit.O2.expect(0)
    tester.circuit.O3.expect(0)
    tester.circuit.I = 1
    tester.eval()
    tester.circuit.O0.expect(1)
    tester.circuit.O1.expect(1)
    tester.circuit.O2.expect(0)
    tester.circuit.O3.expect(0)
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O0.expect(0)
    tester.circuit.O1.expect(0)
    tester.circuit.O2.expect(1)
    tester.circuit.O3.expect(1)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
