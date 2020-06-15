import os
import inspect

import ast_tools

import magma as m
from test_sequential import Register
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
    l0 = inspect.currentframe().f_lineno + 1

    @m.sequential2(pre_passes=[ast_tools.passes.loop_unroll()],
                   post_passes=[
                       ast_tools.passes.debug(dump_source_filename=True,
                                              dump_source_lines=True)])
    class LoopUnroll:
        def __init__(self):
            self.regs = [[Register(4) for _ in range(3)] for _ in range(2)]

        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
            O = self.regs[1][-1]
            for i in ast_tools.macros.unroll(range(2)):
                for j in ast_tools.macros.unroll(range(2)):
                    self.regs[i][2 - j] = self.regs[i][1 - j]
                self.regs[1 - i][0] = self.regs[i][-1] if m.Bit(i == 0) else I
            return O

    assert capsys.readouterr().out == f"""\
BEGIN SOURCE_FILENAME
{os.path.abspath(__file__)}
END SOURCE_FILENAME

BEGIN SOURCE_LINES
{l0+9}:        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
{l0+10}:            O = self.regs[1][-1]
{l0+11}:            for i in ast_tools.macros.unroll(range(2)):
{l0+12}:                for j in ast_tools.macros.unroll(range(2)):
{l0+13}:                    self.regs[i][2 - j] = self.regs[i][1 - j]
{l0+14}:                self.regs[1 - i][0] = self.regs[i][-1] if m.Bit(i == 0) else I
{l0+15}:            return O
END SOURCE_LINES

"""

    m.compile("build/TestSequential2NestedLoopUnroll", LoopUnroll)
    assert check_files_equal(__file__, f"build/TestSequential2NestedLoopUnroll.v",
                             f"gold/TestSequential2NestedLoopUnroll.v")
