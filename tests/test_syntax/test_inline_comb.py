import operator
import os
import fault
from hwtypes import BitVector, Bit, BitVector as BV
import magma as m
from magma.testing import check_files_equal


def test_inline_comb_basic():
    class Main(m.Circuit):
        io = m.IO(invert=m.In(m.Bit), O0=m.Out(m.Bit), O1=m.Out(m.Bit))
        io += m.ClockIO()
        reg = m.Register(m.Bit)()

        O1 = m.Bit()

        @m.inline_combinational(debug=True, file_name="inline_comb.py")
        def logic():
            if io.invert:
                reg.I @= ~reg.O
                O1 @= ~reg.O
            else:
                reg.I @= reg.O
                O1 @= reg.O

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


def test_many_name_gen():
    """
    Ensures that there are no collisions when auto generating names in the
    translation when there are 11 if/else cases and 11 variables.  Before we
    could encounter a collision with prefix111 where it was either case 11, var
    1 or case 1, var 11.  Separating the case/var prefix with an underscore
    avoids this problem

    See https://github.com/phanrahan/magma/pull/835 for some more context
    """

    # Should not raise TypeError from the combinational block
    # E.g. 
    # E           TypeError: ite expects same type for both branches: Out(Bits[12]) != Out(Bits[2])
    class Foo(m.Circuit):
        io = m.IO(
            S=m.In(m.Bits[4]),
            O0=m.Out(m.Bits[1]),
            O1=m.Out(m.Bits[2]),
            O2=m.Out(m.Bits[3]),
            O3=m.Out(m.Bits[4]),
            O4=m.Out(m.Bits[5]),
            O5=m.Out(m.Bits[6]),
            O6=m.Out(m.Bits[7]),
            O7=m.Out(m.Bits[8]),
            O8=m.Out(m.Bits[9]),
            O9=m.Out(m.Bits[10]),
            O10=m.Out(m.Bits[11]),
            O11=m.Out(m.Bits[12])
        )

        @m.inline_combinational()
        def logic():
            io.O0 @= m.bits(0, 1)
            io.O1 @= m.bits(0, 2)
            io.O2 @= m.bits(0, 3)
            io.O3 @= m.bits(0, 4)
            io.O4 @= m.bits(0, 5)
            io.O5 @= m.bits(0, 6)
            io.O6 @= m.bits(0, 7)
            io.O7 @= m.bits(0, 8)
            io.O8 @= m.bits(0, 9)
            io.O9 @= m.bits(0, 10)
            io.O10 @= m.bits(0, 11)
            io.O11 @= m.bits(0, 12)
            if io.S == 0:
                io.O0 @= m.bits(1, 1)
                io.O1 @= m.bits(1, 2)
                io.O2 @= m.bits(1, 3)
                io.O3 @= m.bits(1, 4)
                io.O4 @= m.bits(1, 5)
                io.O5 @= m.bits(1, 6)
                io.O6 @= m.bits(1, 7)
                io.O7 @= m.bits(1, 8)
                io.O8 @= m.bits(1, 9)
                io.O9 @= m.bits(1, 10)
                io.O10 @= m.bits(1, 11)
                io.O11 @= m.bits(1, 12)
            elif io.S == 1:
                io.O0 @= m.bits(0, 1)
                io.O1 @= m.bits(0, 2)
                io.O2 @= m.bits(0, 3)
                io.O3 @= m.bits(0, 4)
                io.O4 @= m.bits(0, 5)
                io.O5 @= m.bits(0, 6)
                io.O6 @= m.bits(0, 7)
                io.O7 @= m.bits(0, 8)
                io.O8 @= m.bits(0, 9)
                io.O9 @= m.bits(0, 10)
                io.O10 @= m.bits(0, 11)
                io.O11 @= m.bits(0, 12)
            elif io.S == 2:
                io.O0 @= m.bits(1, 1)
                io.O1 @= m.bits(1, 2)
                io.O2 @= m.bits(1, 3)
                io.O3 @= m.bits(1, 4)
                io.O4 @= m.bits(1, 5)
                io.O5 @= m.bits(1, 6)
                io.O6 @= m.bits(1, 7)
                io.O7 @= m.bits(1, 8)
                io.O8 @= m.bits(1, 9)
                io.O9 @= m.bits(1, 10)
                io.O10 @= m.bits(1, 11)
                io.O11 @= m.bits(1, 12)
            elif io.S == 3:
                io.O0 @= m.bits(0, 1)
                io.O1 @= m.bits(0, 2)
                io.O2 @= m.bits(0, 3)
                io.O3 @= m.bits(0, 4)
                io.O4 @= m.bits(0, 5)
                io.O5 @= m.bits(0, 6)
                io.O6 @= m.bits(0, 7)
                io.O7 @= m.bits(0, 8)
                io.O8 @= m.bits(0, 9)
                io.O9 @= m.bits(0, 10)
                io.O10 @= m.bits(0, 11)
                io.O11 @= m.bits(0, 12)
            elif io.S == 4:
                io.O0 @= m.bits(1, 1)
                io.O1 @= m.bits(1, 2)
                io.O2 @= m.bits(1, 3)
                io.O3 @= m.bits(1, 4)
                io.O4 @= m.bits(1, 5)
                io.O5 @= m.bits(1, 6)
                io.O6 @= m.bits(1, 7)
                io.O7 @= m.bits(1, 8)
                io.O8 @= m.bits(1, 9)
                io.O9 @= m.bits(1, 10)
                io.O10 @= m.bits(1, 11)
                io.O11 @= m.bits(1, 12)
            elif io.S == 5:
                io.O0 @= m.bits(0, 1)
                io.O1 @= m.bits(0, 2)
                io.O2 @= m.bits(0, 3)
                io.O3 @= m.bits(0, 4)
                io.O4 @= m.bits(0, 5)
                io.O5 @= m.bits(0, 6)
                io.O6 @= m.bits(0, 7)
                io.O7 @= m.bits(0, 8)
                io.O8 @= m.bits(0, 9)
                io.O9 @= m.bits(0, 10)
                io.O10 @= m.bits(0, 11)
                io.O11 @= m.bits(0, 12)
            elif io.S == 6:
                io.O0 @= m.bits(1, 1)
                io.O1 @= m.bits(1, 2)
                io.O2 @= m.bits(1, 3)
                io.O3 @= m.bits(1, 4)
                io.O4 @= m.bits(1, 5)
                io.O5 @= m.bits(1, 6)
                io.O6 @= m.bits(1, 7)
                io.O7 @= m.bits(1, 8)
                io.O8 @= m.bits(1, 9)
                io.O9 @= m.bits(1, 10)
                io.O10 @= m.bits(1, 11)
                io.O11 @= m.bits(1, 12)
            elif io.S == 7:
                io.O0 @= m.bits(0, 1)
                io.O1 @= m.bits(0, 2)
                io.O2 @= m.bits(0, 3)
                io.O3 @= m.bits(0, 4)
                io.O4 @= m.bits(0, 5)
                io.O5 @= m.bits(0, 6)
                io.O6 @= m.bits(0, 7)
                io.O7 @= m.bits(0, 8)
                io.O8 @= m.bits(0, 9)
                io.O9 @= m.bits(0, 10)
                io.O10 @= m.bits(0, 11)
                io.O11 @= m.bits(0, 12)
            elif io.S == 8:
                io.O0 @= m.bits(1, 1)
                io.O1 @= m.bits(1, 2)
                io.O2 @= m.bits(1, 3)
                io.O3 @= m.bits(1, 4)
                io.O4 @= m.bits(1, 5)
                io.O5 @= m.bits(1, 6)
                io.O6 @= m.bits(1, 7)
                io.O7 @= m.bits(1, 8)
                io.O8 @= m.bits(1, 9)
                io.O9 @= m.bits(1, 10)
                io.O10 @= m.bits(1, 11)
                io.O11 @= m.bits(1, 12)
            elif io.S == 9:
                io.O0 @= m.bits(0, 1)
                io.O1 @= m.bits(0, 2)
                io.O2 @= m.bits(0, 3)
                io.O3 @= m.bits(0, 4)
                io.O4 @= m.bits(0, 5)
                io.O5 @= m.bits(0, 6)
                io.O6 @= m.bits(0, 7)
                io.O7 @= m.bits(0, 8)
                io.O8 @= m.bits(0, 9)
                io.O9 @= m.bits(0, 10)
                io.O10 @= m.bits(0, 11)
                io.O11 @= m.bits(0, 12)
            elif io.S == 10:
                io.O0 @= m.bits(1, 1)
                io.O1 @= m.bits(1, 2)
                io.O2 @= m.bits(1, 3)
                io.O3 @= m.bits(1, 4)
                io.O4 @= m.bits(1, 5)
                io.O5 @= m.bits(1, 6)
                io.O6 @= m.bits(1, 7)
                io.O7 @= m.bits(1, 8)
                io.O8 @= m.bits(1, 9)
                io.O9 @= m.bits(1, 10)
                io.O10 @= m.bits(1, 11)
                io.O11 @= m.bits(1, 12)
            elif io.S == 11:
                io.O0 @= m.bits(0, 1)
                io.O1 @= m.bits(0, 2)
                io.O2 @= m.bits(0, 3)
                io.O3 @= m.bits(0, 4)
                io.O4 @= m.bits(0, 5)
                io.O5 @= m.bits(0, 6)
                io.O6 @= m.bits(0, 7)
                io.O7 @= m.bits(0, 8)
                io.O8 @= m.bits(0, 9)
                io.O9 @= m.bits(0, 10)
                io.O10 @= m.bits(0, 11)
                io.O11 @= m.bits(0, 12)
