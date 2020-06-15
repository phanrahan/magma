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


def test_sequential2_pre_unroll():
    @m.sequential2(pre_passes=[ast_tools.passes.loop_unroll()])
    class LoopUnroll:
        def __init__(self):
            self.regs = [Register(4) for _ in range(3)]

        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
            O = self.regs[2]
            for j in ast_tools.macros.unroll(range(2)):
                self.regs[2 - j] = self.regs[1 - j]
            self.regs[0] = I
            return O

    m.compile("build/TestSequential2LoopUnroll", LoopUnroll)
    assert check_files_equal(__file__, f"build/TestSequential2LoopUnroll.v",
                             f"gold/TestSequential2LoopUnroll.v")
