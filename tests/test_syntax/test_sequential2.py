import tempfile
import os
import inspect

import ast_tools
import fault

import magma as m
from test_sequential import Register, DualClockRAM
from magma.testing import check_files_equal


def test_sequential2_basic():
    @m.sequential2()
    class Basic:
        def __init__(self):
            self.x = Register(4)
            self.y = Register(4)

        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
            return self.y(self.x(I))

    m.compile("build/TestSequential2Basic", Basic)
    assert check_files_equal(__file__, f"build/TestSequential2Basic.v",
                             f"gold/TestSequential2Basic.v")


def test_sequential2_assign():
    @m.sequential2()
    class Basic:
        def __init__(self):
            self.x = Register(4)
            self.y = Register(4)

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
            self.x = Register(4)
            self.y = Register(4)

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
                self.regs = [[Register(4) for _ in range(3)] for _ in range(2)]

            def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
                O = self.regs[1][-1]
                for i in ast_tools.macros.unroll(range(y)):
                    for j in ast_tools.macros.unroll(range(2)):
                        self.regs[1 - i][2 - j] = self.regs[1 - i][1 - j]
                    self.regs[1 - i][0] = self.regs[i][-1] if m.Bit(i == 0) else I
                return O

        with open(os.path.join(tmpdir, "foo.py"), "r") as output:
            assert output.read() == """\
def __call__(self, I: m.Bits[4]) ->m.Bits[4]:
    O0 = self.regs[1][-1]
    self.regs[1 - 0][2 - 0] = self.regs[1 - 0][1 - 0]
    self.regs[1 - 0][2 - 1] = self.regs[1 - 0][1 - 1]
    self.regs[1 - 0][0] = __phi(m.Bit(0 == 0), self.regs[0][-1], I)
    self.regs[1 - 1][2 - 0] = self.regs[1 - 1][1 - 0]
    self.regs[1 - 1][2 - 1] = self.regs[1 - 1][1 - 1]
    self.regs[1 - 1][0] = __phi(m.Bit(1 == 0), self.regs[1][-1], I)
    __return_value0 = O0
    return __return_value0
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
    class ImplicitClock:
        def __call__(self, WCLK: m.Clock, RCLK: m.Clock) -> m.Bits[8]:
            rdata = DualClockRAM()(
                RADDR=m.bits(0, 8),
                WADDR=m.bits(0, 8),
                WDATA=m.bits(0, 8),
                WE=m.bit(0),
                # Always the first Clock argument will be wired up implicitly
                # RCLK=WCLK
                # WCLK=WCLK
            )
            return rdata

    m.compile("build/TestSequential2ImplicitClock", ImplicitClock)
    assert check_files_equal(__file__,
                             f"build/TestSequential2ImplicitClock.v",
                             f"gold/TestSequential2ImplicitClock.v")

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
            self.x = Register(4)
            self.y = Register(4)

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
            self.x = Register(4)
            self.y = Register(4)

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
                return m.namedtuple(a=m.bit(0))
            else:
                return m.namedtuple(a=m.bit(1))

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


def test_sequential2_ite():
    @m.sequential2()
    class Test:
        def __init__(self):
            self.v = m.Register(T=m.Bit, init=m.bit(0))()

        def __call__(self, sel: m.Bit) -> m.AnonProduct[dict(a=m.Bit)]:
            self.v = sel
            if sel:
                return m.namedtuple(a=self.v.prev())
            else:
                return m.namedtuple(a=self.v.prev())

    m.compile("build/TestSequential2Ite", Test, inline=True)
    assert check_files_equal(__file__, f"build/TestSequential2Ite.v",
                             f"gold/TestSequential2Ite.v")
