import operator
import tempfile
import os
import inspect
import pytest

import pytest
import ast_tools
import fault
from hwtypes import UIntVector

import magma as m
from magma.testing import check_files_equal

Register = m.Register

from ast_tools import SymbolTable

class DualClockRAM(m.Circuit):
    io = m.IO(
        RADDR=m.In(m.Bits[8]),
        WADDR=m.In(m.Bits[8]),
        WDATA=m.In(m.Bits[8]),
        RDATA=m.Out(m.Bits[8]),
        WE=m.In(m.Bit),
        RCLK=m.In(m.Clock),
        WCLK=m.In(m.Clock)
    )

    m.wire(m.bits(0, 8), io.RDATA)


def test_sequential2_basic():
    @m.sequential2()
    class Basic:
        def __init__(self):
            self.x = Register(m.Bits[4])()
            self.y = Register(m.Bits[4])()

        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
            return self.y(self.x(I))

    m.compile("build/TestSequential2Basic", Basic)
    assert check_files_equal(__file__, f"build/TestSequential2Basic.v",
                             f"gold/TestSequential2Basic.v")


def test_sequential2_assign():
    @m.sequential2()
    class Basic:
        def __init__(self):
            self.x = Register(m.Bits[4])()
            self.y = Register(m.Bits[4])()

        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
            O = self.y
            self.y = self.x
            self.x = I
            return O

    m.compile("build/TestSequential2Assign", Basic)
    assert check_files_equal(__file__, f"build/TestSequential2Assign.v",
                             f"gold/TestSequential2Assign.v")

    # should be the same as basic
    assert check_files_equal(__file__, f"build/TestSequential2Assign.v",
                             f"gold/TestSequential2Basic.v")


def test_sequential2_hierarchy():
    @m.sequential2()
    class Foo:
        def __init__(self):
            self.x = Register(m.Bits[4])()
            self.y = Register(m.Bits[4])()

        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
            return self.y(self.x(I))


    @m.sequential2()
    class Bar:
        def __init__(self):
            self.x = Foo()
            self.y = Foo()

        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
            return self.y(self.x(I))

    m.compile("build/TestSequential2Hierarchy", Bar)
    assert check_files_equal(__file__, f"build/TestSequential2Hierarchy.v",
                             f"gold/TestSequential2Hierarchy.v")


def test_sequential2_pre_unroll(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        l0 = inspect.currentframe().f_lineno + 1

        @m.sequential2(pre_passes=[ast_tools.passes.loop_unroll()],
                       post_passes=[
                           ast_tools.passes.debug(dump_source_filename=True,
                                                  dump_source_lines=True)],
                       env=locals().update(y=2),
                       debug=True, path=tmpdir, file_name="foo.py")
        class LoopUnroll:
            def __init__(self):
                self.regs = [[Register(m.Bits[4])() for _ in range(3)] for _ in range(2)]

            def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
                O = self.regs[1][-1]
                for i in ast_tools.macros.unroll(range(y)):
                    for j in ast_tools.macros.unroll(range(2)):
                        self.regs[1 - i][2 - j] = self.regs[1 - i][1 - j]
                    self.regs[1 - i][0] = self.regs[i][-1] if m.Bit(i == 0) else I
                return O

        with open(os.path.join(tmpdir, "foo.py"), "r") as output:
            assert output.read() == """\
def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
    O_0 = self.regs[1][-1]
    self.regs[1 - 0][2 - 0] = self.regs[1 - 0][1 - 0]
    self.regs[1 - 0][2 - 1] = self.regs[1 - 0][1 - 1]
    self.regs[1 - 0][0] = __phi(m.Bit(0 == 0), self.regs[0][-1], I)
    self.regs[1 - 1][2 - 0] = self.regs[1 - 1][1 - 0]
    self.regs[1 - 1][2 - 1] = self.regs[1 - 1][1 - 1]
    self.regs[1 - 1][0] = __phi(m.Bit(1 == 0), self.regs[1][-1], I)
    __0_return_0 = O_0
    return __0_return_0
"""

    assert capsys.readouterr().out == f"""\
BEGIN SOURCE_FILENAME
{os.path.abspath(__file__)}
END SOURCE_FILENAME

BEGIN SOURCE_LINES
{l0+11}:            def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
{l0+12}:                O = self.regs[1][-1]
{l0+13}:                for i in ast_tools.macros.unroll(range(y)):
{l0+14}:                    for j in ast_tools.macros.unroll(range(2)):
{l0+15}:                        self.regs[1 - i][2 - j] = self.regs[1 - i][1 - j]
{l0+16}:                    self.regs[1 - i][0] = self.regs[i][-1] if m.Bit(i == 0) else I
{l0+17}:                return O
END SOURCE_LINES

"""

    m.compile("build/TestSequential2NestedLoopUnroll", LoopUnroll)
    assert check_files_equal(__file__, f"build/TestSequential2NestedLoopUnroll.v",
                             f"gold/TestSequential2NestedLoopUnroll.v")


def test_dual_clock_ram():
    @m.sequential2()
    class DefaultClock:
        def __call__(self) -> m.Bits[8]:
            rdata = DualClockRAM()(
                RADDR=m.bits(0, 8),
                WADDR=m.bits(0, 8),
                WDATA=m.bits(0, 8),
                WE=m.bit(0),
                # Default CLK will be wired up implicitly
                # RCLK=CLK
                # WCLK=CLK
            )
            return rdata

    m.compile("build/TestSequential2DefaultClock", DefaultClock)
    assert check_files_equal(__file__,
                             f"build/TestSequential2DefaultClock.v",
                             f"gold/TestSequential2DefaultClock.v")

    @m.sequential2()
    class ExplicitClock:
        def __call__(self, WCLK: m.Clock, RCLK: m.Clock) -> m.Bits[8]:
            rdata = DualClockRAM()(
                RADDR=m.bits(0, 8),
                WADDR=m.bits(0, 8),
                WDATA=m.bits(0, 8),
                WE=m.bit(0),
                # Wiring clocks explicitly
                RCLK=RCLK,
                WCLK=WCLK
            )
            return rdata

    m.compile("build/TestSequential2ExplicitClock", ExplicitClock)
    assert check_files_equal(__file__,
                             f"build/TestSequential2ExplicitClock.v",
                             f"gold/TestSequential2ExplicitClock.v")


def test_sequential2_return_tuple():
    @m.sequential2()
    class Basic:
        def __init__(self):
            self.x = Register(m.Bits[4])()
            self.y = Register(m.Bits[4])()

        def __call__(self, I: m.Bits[4], S: m.Bit) -> (m.Bits[4], m.Bits[4]):
            self.y = self.x
            self.x = I
            if S:
                return self.x, self.y
            else:
                return self.y, self.x

    m.compile("build/TestSequential2ReturnTuple", Basic, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2ReturnTuple.v",
                             f"gold/TestSequential2ReturnTuple.v")


def test_sequential2_custom_annotations():
    annotations = {"I": m.Bits[4], "S": m.Bit, "return": m.Bits[4]}
    @m.sequential2(annotations=annotations)
    class Basic:
        def __init__(self):
            self.x = Register(m.Bits[4])()
            self.y = Register(m.Bits[4])()

        # Bad annotations to make sure they're overridden
        def __call__(self, I: int, S: str) -> tuple:
            O = self.y
            self.y = self.x
            self.x = I
            return O

    m.compile("build/TestSequential2CustomAnnotations", Basic, inline=True)
    assert check_files_equal(__file__,
                             f"build/TestSequential2CustomAnnotations.v",
                             f"gold/TestSequential2CustomAnnotations.v")


def test_sequential2_counter():
    @m.sequential2()
    class Test2:
        def __init__(self):
            self.count = m.Register(T=m.SInt[16], init=m.sint(0, 16))()

        def __call__(self) -> m.SInt[16]:
            self.count = self.count + 1
            return self.count

    m.compile("build/TestSequential2Counter", Test2, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2Counter.v",
                             f"gold/TestSequential2Counter.v")


def test_sequential2_counter_if():
    @m.sequential2()
    class Test2:
        def __init__(self):
            self.count = m.Register(T=m.SInt[16], init=m.sint(0, 16))()

        def __call__(self, sel: m.Bit) -> m.SInt[16]:
            if sel:
                self.count = self.count + 1
            return self.count

    m.compile("build/TestSequential2CounterIf", Test2, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2CounterIf.v",
                             f"gold/TestSequential2CounterIf.v")


def test_sequential2_product():
    @m.sequential2()
    class Test:
        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bit)]:
            if sel:
                return m.product(a=m.bit(0))
            else:
                return m.product(a=m.bit(1))

    m.compile("build/TestSequential2Product", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2Product.v",
                             f"gold/TestSequential2Product.v")


def test_sequential2_arr_of_bits():
    T = m.Array[15, m.Bits[7]]
    @m.sequential2()
    class Test2:
        def __init__(self):
            self.reg_arr = m.Register(T=T)()

        def __call__(self, I: T) -> T:
            O = self.reg_arr
            self.reg_arr = I
            return O

    m.compile("build/TestSequential2ArrOfBits", Test2, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2ArrOfBits.v",
                             f"gold/TestSequential2ArrOfBits.v")


def test_sequential2_getitem():
    T = m.Array[8, m.Bits[7]]
    @m.sequential2()
    class Test2:
        def __init__(self):
            self.reg_arr = m.Register(T=T)()
            self.index = m.Register(T=m.Bits[3])()

        def __call__(self, I: T, index: m.Bits[3]) -> m.Array[2, m.Bits[7]]:
            out = m.array([self.reg_arr[index], self.reg_arr[self.index]])
            self.reg_arr = I
            self.index = index
            return out

    m.compile("build/TestSequential2GetItem", Test2, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2GetItem.v",
                             f"gold/TestSequential2GetItem.v")


def test_sequential2_slice():
    @m.sequential2()
    class TestSequential2Slice:
        def __init__(self):
            self.mem = m.Register(T=m.Bits[8 * 8])()

        def __call__(self, write_addr: m.UInt[3], write_data: m.Bits[8],
                     read_addr: m.UInt[3]) -> m.Bits[8]:
            read_data = m.get_slice(self.mem, m.zext(read_addr, 3) * 8, 8)
            self.mem = m.set_slice(self.mem, write_data,
                                   m.zext(write_addr, 3) * 8, 8)
            return read_data

    m.compile("build/TestSequential2Slice", TestSequential2Slice, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2Slice.v",
                             f"gold/TestSequential2Slice.v")

    tester = fault.SynchronousTester(TestSequential2Slice,
                                     TestSequential2Slice.CLK)
    tester.circuit.write_addr = 1
    tester.circuit.write_data = 2
    tester.circuit.read_addr = 1
    tester.advance_cycle()
    tester.circuit.O.expect(2)
    tester.circuit.write_addr = 2
    tester.circuit.write_data = 3
    tester.circuit.read_addr = 2
    tester.advance_cycle()
    tester.circuit.O.expect(3)
    # Check addr 1 wasn't overwriten
    tester.circuit.read_addr = 1
    tester.advance_cycle()
    tester.circuit.O.expect(2)

    build_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "build"
    )
    tester.compile_and_run("verilator", skip_compile=True, directory=build_dir,
                           flags=["-Wno-unused"])


def test_sequential2_prev():
    @m.sequential2()
    class Test2:
        def __init__(self):
            self.cnt = m.Register(T=m.UInt[3])()

        def __call__(self) -> m.UInt[3]:
            self.cnt = self.cnt + 1
            return self.cnt.prev()

    m.compile("build/TestSequential2Prev", Test2, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2Prev.v",
                             f"gold/TestSequential2Prev.v")


def test_sequential2_reset():
    @m.sequential2(reset_type=m.AsyncReset, has_enable=True)
    class Test2:
        def __init__(self):
            # reset_type and has_enable will be set implicitly
            self.cnt = m.Register(T=m.UInt[3])()

        def __call__(self) -> m.UInt[3]:
            self.cnt = self.cnt + 1
            return self.cnt

    m.compile("build/TestSequential2Reset", Test2, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2Reset.v",
                             f"gold/TestSequential2Reset.v")


def test_sequential2_ite_array():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.Array[1, m.Bit]:
            self.v = sel
            if sel:
                return m.array([m.bit(0)])
            else:
                return m.array([self.v.prev()])

    m.compile("build/TestSequential2IteArray", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteArray.v",
                             f"gold/TestSequential2IteArray.v")


def test_sequential2_ite_array2():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.Array[2, m.Bit]:
            self.v = sel
            if sel:
                return m.array([m.bit(0), m.bit(0)])
            else:
                return m.array([self.v.prev(), m.bit(1)])

    m.compile("build/TestSequential2IteArray2", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteArray2.v",
                             f"gold/TestSequential2IteArray2.v")


def test_sequential2_ite_array_error():
    with pytest.raises(TypeError,
                       match="Found incompatible types .* in mux inference"):
        @m.sequential2()
        class Test:
            def __init__(self):
                self.v = m.Register(T=m.Bit, init=m.bit(0))()

            def __call__(self, sel: m.Bit) -> m.Array[1, m.Bit]:
                self.v = sel
                if sel:
                    return m.array([m.bit(0), m.bit(0)])
                else:
                    return m.array([self.v.prev()])


def test_sequential2_ite_tuple():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.Tuple[m.Bit]:
            self.v = sel
            if sel:
                return m.tuple_(self.v.prev())
            else:
                return m.tuple_(self.v.prev())

    m.compile("build/TestSequential2IteTuple", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteTuple.v",
                             f"gold/TestSequential2IteTuple.v")


def test_sequential2_ite_tuple2():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.Tuple[m.Bit]:
            self.v = sel
            if sel:
                return m.tuple_(m.bit(0))
            else:
                return m.tuple_(self.v.prev())

    m.compile("build/TestSequential2IteTuple2", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteTuple2.v",
                             f"gold/TestSequential2IteTuple2.v")


def test_sequential2_ite_tuple_error_type():
    with pytest.raises(TypeError,
                       match="Found incompatible types .* in mux inference"):
        @m.sequential2()
        class Test:
            def __init__(self):
                self.v = m.Register(T=m.Bit, init=m.bit(0))()

            def __call__(self, sel: m.Bit) -> m.Tuple[m.Bit]:
                self.v = sel
                if sel:
                    return m.tuple_(m.bits(0, 2))
                else:
                    return m.tuple_(self.v.prev())


def test_sequential2_ite_product():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bit)]:
            self.v = sel
            if sel:
                return m.product(a=self.v.prev())
            else:
                return m.product(a=self.v.prev())

    m.compile("build/TestSequential2IteProduct", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteProduct.v",
                             f"gold/TestSequential2IteProduct.v")


def test_sequential2_ite_product2():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bit)]:
            self.v = sel
            if sel:
                return m.product(a=m.bit(0))
            else:
                return m.product(a=self.v.prev())

    m.compile("build/TestSequential2IteProduct2", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteProduct2.v",
                             f"gold/TestSequential2IteProduct2.v")


def test_sequential2_ite_product_error_type():
    with pytest.raises(TypeError,
                       match="Found incompatible types .* in mux inference"):
        @m.sequential2()
        class Test:
            def __init__(self):
                self.v = m.Register(T=m.Bit, init=m.bit(0))()

            def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bit)]:
                self.v = sel
                if sel:
                    return m.product(a=m.bits(0, 2))
                else:
                    return m.product(a=self.v.prev())


def test_sequential2_ite_product_error_keys():
    with pytest.raises(TypeError,
                       match="Found incompatible types .* in mux inference"):
        @m.sequential2()
        class Test:
            def __init__(self):
                self.v = m.Register(T=m.Bit, init=m.bit(0))()

            def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bit)]:
                self.v = sel
                if sel:
                    return m.product(a=m.bit(0))
                else:
                    return m.product(b=self.v.prev())


def test_sequential2_ite_nested():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(
            a=m.AnonProduct[dict(b=m.Bit)],
            c=m.Tuple[m.Bit])
        ]:
            self.v = sel
            if sel:
                return m.product(a=m.product(b=m.bit(0)),
                                    c=m.tuple_(m.bit(0)))
            else:
                return m.product(a=m.product(b=self.v.prev()),
                                    c=m.tuple_(self.v.prev()))

    m.compile("build/TestSequential2IteNested", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteNested.v",
                             f"gold/TestSequential2IteNested.v")


def test_sequential2_ite_bits():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bits[8], init=m.bits(0, 8))()

        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bits[8])]:
            self.v = self.v
            if sel:
                return m.product(a=self.v.prev())
            else:
                return m.product(a=self.v.prev())

    m.compile("build/TestSequential2IteBits", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteBits.v",
                             f"gold/TestSequential2IteBits.v")


def test_sequential2_ite_bits2():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bits[8], init=m.bits(0, 8))()

        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bits[8])]:
            self.v = self.v
            if sel:
                return m.product(a=m.bits(0, 8))
            else:
                return m.product(a=self.v.prev())

    m.compile("build/TestSequential2IteBits2", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteBits2.v",
                             f"gold/TestSequential2IteBits2.v")


def test_sequential2_ite_bits3():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bits[8])]:
            self.v = self.v
            if sel:
                return m.product(a=m.concat(m.bits(0, 4),
                                               m.repeat(self.v.prev(), 3),
                                               self.v.prev()))
            else:
                return m.product(a=m.bits(self.v.prev(), 8))

    m.compile("build/TestSequential2IteBits3", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteBits3.v",
                             f"gold/TestSequential2IteBits3.v")


def test_sequential2_ite_complex():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.a = m.Register(T=m.Bit, init=m.bit(0))()
            self.b = m.Register(T=m.Bits[2], init=m.bits(0, 2))()

        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(
                                              a=m.Tuple[m.Bits[2]],
                                              b=m.Array[2, m.Bit],
                                          )]:
            self.a = self.a
            self.b = self.b
            if sel:
                return m.product(
                           a=m.tuple_([self.b.prev()]),
                           b=m.array([self.a.prev(), self.a.prev()]),
                       )
            else:
                return m.product(
                           a=m.tuple_([m.array([self.a.prev(), self.a.prev()])]),
                           b=m.array(self.b.prev()),
                       )

    m.compile("build/TestSequential2IteComplex", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteComplex.v",
                             f"gold/TestSequential2IteComplex.v")


def test_sequential2_ite_complex_register():
    class T(m.Product):
        a = m.Array[1, m.Bits[2]]
        b = m.Tuple[m.AnonProduct[dict(c=m.Array[2, m.Bit])]]

    @m.sequential2()
    class Test:
        def __init__(self):
            self.a = m.Register(
                T=T,
                init=m.product(
                    a=m.array([m.bits(0, 2)]),
                    b=m.tuple_([m.product(c=m.array([m.bit(0), m.bit(0)]))]),
                ),
            )()

        def __call__(self, sel: m.Bit) -> T:
            self.a = self.a
            if sel:
                return self.a
            else:
                return self.a

    m.compile("build/TestSequential2IteComplexRegister", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteComplexRegister.v",
                             f"gold/TestSequential2IteComplexRegister.v")


def test_sequential2_ite_complex_register2():
    class T(m.Product):
        a = m.Array[1, m.Bits[2]]
        b = m.Tuple[m.AnonProduct[dict(c=m.Array[2, m.Bit])]]

    @m.sequential2()
    class Test:
        def __init__(self):
            self.a = m.Register(
                T=T,
                init=m.product(
                    a=m.array([m.bits(0, 2)]),
                    b=m.tuple_([m.product(c=m.array([m.bit(0), m.bit(0)]))]),
                ),
            )()

        def __call__(self, sel: m.Bit) -> T:
            self.a = self.a
            if sel:
                return m.product(
                    a=m.array([self.a.b[0].c]),
                    b=m.tuple_([m.product(
                        c=m.array([m.bit(0), m.bit(self.a.a[0][1:2])]))]
                    ),
                )
            else:
                return self.a

    m.compile("build/TestSequential2IteComplexRegister2", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2IteComplexRegister2.v",
                             f"gold/TestSequential2IteComplexRegister2.v")


def test_gcd():
    @m.sequential2()
    class GCD:
        def __init__(self):
            self.x = m.Register(m.UInt[16])()
            self.y = m.Register(m.UInt[16])()

        def __call__(self, a: m.In(m.UInt[16]), b: m.In(m.UInt[16]),
                     load: m.In(m.Bit)) -> (m.Out(m.UInt[16]), m.Out(m.Bit)):
            if load:
                self.x = a
                self.y = b
            elif self.y != 0:
                if self.x > self.y:
                    self.x = self.x - self.y
                else:
                    self.y = self.y - self.x
            return self.x.prev(), self.y.prev() == 0

    m.compile("build/GCD", GCD, inline=True)
    tester = fault.SynchronousTester(GCD, clock=GCD.CLK)
    tester.circuit.a = 32
    tester.circuit.b = 16
    tester.circuit.load = 1
    tester.advance_cycle()
    tester.circuit.load = 0
    tester.advance_cycle()
    tester.wait_on(tester.circuit.O1 == 1)
    tester.circuit.O0.expect(16)
    dir_ = os.path.join(os.path.dirname(__file__), "build")
    tester.compile_and_run("verilator", skip_compile=True, directory=dir_,
                           flags=["-Wno-unused"])


@pytest.mark.parametrize('op', [operator.add, operator.sub, operator.mul,
                                operator.floordiv, operator.truediv,
                                operator.mod, operator.lshift, operator.rshift,
                                operator.and_, operator.xor, operator.or_])
def test_r_ops(op):
    @m.sequential2()
    class Test:
        def __init__(self):
            self.x = m.Register(m.UInt[16])()
            self.y = m.Register(m.UInt[16])()

        def __call__(self, a: m.In(m.UInt[16]), b: m.In(m.UInt[16]),
                     load: m.In(m.Bit)) -> (m.Out(m.UInt[16]),
                                            m.Out(m.UInt[16])):
            if load:
                self.x = a
                self.y = b
            else:
                self.x = op(self.x, self.y)
                self.y = op(self.y, self.x)
            return self.x.prev(), self.y.prev()

    type(Test).rename(Test, f"TestRop{op.__name__}")
    m.compile(f"build/TestRop{op.__name__}", Test, inline=True)
    if op in {operator.mod, operator.truediv}:
        # coreir doesn't support urem primitive
        # hwtypes BV doesn't support truediv
        # but we still test these right hand op implementation for coverage and
        # to make sure they compile without error
        return
    tester = fault.SynchronousTester(Test, clock=Test.CLK)
    tester.circuit.a = a = 32
    tester.circuit.b = b = 3
    tester.circuit.load = 1
    tester.advance_cycle()
    tester.circuit.load = 0
    tester.advance_cycle()
    O0 = op(a, b)
    tester.circuit.O0.expect(O0)
    tester.circuit.O1.expect(op(b, O0))
    dir_ = os.path.join(os.path.dirname(__file__), "build")
    tester.compile_and_run("verilator", flags=['-Wno-unused'],
                           skip_compile=True, directory=dir_)


@pytest.mark.parametrize('op', [operator.invert, operator.neg])
def test_u_ops(op):
    @m.sequential2()
    class Test:
        def __init__(self):
            self.x = m.Register(m.SInt[16])()

        def __call__(self, a: m.In(m.SInt[16]),
                     load: m.In(m.Bit)) -> m.Out(m.SInt[16]):
            if load:
                self.x = a
            else:
                self.x = op(self.x)
            return self.x.prev()

    type(Test).rename(Test, f"TestUop{op.__name__}")
    m.compile(f"build/TestUop{op.__name__}", Test, inline=True)
    tester = fault.SynchronousTester(Test, clock=Test.CLK)
    tester.circuit.a = a = 32
    tester.circuit.load = 1
    tester.advance_cycle()
    tester.circuit.load = 0
    tester.advance_cycle()
    O = op(a)
    tester.circuit.O.expect(O)
    dir_ = os.path.join(os.path.dirname(__file__), "build")
    tester.compile_and_run("verilator", flags=['-Wno-unused'],
                           skip_compile=True, directory=dir_)


def test_reset_no_init():
    Data = m.UInt[8]

    @m.sequential2(reset_type=m.AsyncReset)
    class Inc:
        def __call__(self, i: Data) -> Data:
            return i + 1


def test_magma_not_in_env():

    Data = m.UInt[8]
    env = SymbolTable({}, {'Data': Data})

    @m.sequential2(env=env, reset_type=m.AsyncReset)
    class Inc:
        def __init__(self):
            pass

        def __call__(self, i: Data) -> Data:
            return i + 1


def test_named_outputs():
    Data = m.UInt[8]
    @m.sequential2(output_port_names=['s','c_out'])
    class Adder:
        def __call__(self, a: Data, b: Data, c_in: m.Bit) -> (Data, m.Bit):
            return a.adc(b, c_in)

    assert Adder.interface.ports.keys() == {'a', 'b', 'c_in', 's', 'c_out', 'CLK'}
