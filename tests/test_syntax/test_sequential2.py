import magma as m
from test_sequential import Register
from magma.testing import check_files_equal

from ast_tools.passes import begin_rewrite, end_rewrite, ssa


def test_sequential2_basic():
    class Basic(m.SequentialCircuit):

        def __init__(self, width):
            super().__init__()
            self.io = m.IO(opcode=m.In(m.UInt[3]), I=m.In(m.Bits[width]),
                           out=m.Out(m.Bits[width])) + m.ClockIO(has_ce=True)
            self.x = Register(width, has_ce=True)
            self.y = Register(width, has_ce=True)
            self.x.CE @= self.io.opcode >= 2
            self.y.CE @= self.io.opcode == 3
            # Override default O
            self._call_output_name_ = "out"

        def __call__(self, I):
            # TODO: Register assign syntax, e.g. self.y = self.x
            return self.y(self.x(I))

    m.compile("build/TestSequential2Basic", Basic(4))
    assert check_files_equal(__file__, f"build/TestSequential2Basic.v",
                             f"gold/TestSequential2Basic.v")
