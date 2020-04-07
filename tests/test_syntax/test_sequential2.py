import magma as m
from test_sequential import Register
from magma.testing import check_files_equal

from ast_tools.passes import begin_rewrite, end_rewrite, ssa


def test_sequential2_basic():
    @m.sequential2()
    class Basic:
        def __init__(self):
            self.x = Register(4)
            self.y = Register(4)

        def __call__(self, I: m.Bits[4]) -> m.Bits[4]:
            # TODO: Register assign syntax, e.g. self.y = self.x
            return self.y(self.x(I))

    m.compile("build/TestSequential2Basic", Basic)
    assert check_files_equal(__file__, f"build/TestSequential2Basic.v",
                             f"gold/TestSequential2Basic.v")
