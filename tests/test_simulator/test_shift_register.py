from magma import *
from magma.primitives import DefineRegister

from magma.simulator import PythonSimulator
from magma.scope import Scope
from magma.bit_vector import BitVector
from magma.bitutils import int2seq, seq2int

def test_shift_register():
    N = 4
    Register4 = DefineRegister(4)
    T = Bits(N)

    class ShiftRegister(Circuit):
        name = "ShiftRegister"
        IO = ["I", In(T), "O", Out(T), "CLK", In(Bit)]
        @classmethod
        def definition(io):
            regs = [Register4() for _ in range(N)]
            [wire(io.CLK, reg.clk) for reg in regs]  # TODO: Clean up this clock wiring
            wire(io.I, getattr(regs[0], "in"))
            fold(regs, foldargs={"in":"out"})
            wire(getattr(regs[-1], "out"), io.O)

    simulator = PythonSimulator(ShiftRegister)
    scope = Scope()
    expected = [0, 0, 0] + list(range(0, 1 << N, 3))[:-3]
    actual = []
    for i in range(0, 1 << N, 3):
        simulator.set_value(ShiftRegister.I, scope, uint(i, N))
        for j in range(2):
            simulator.step()
            simulator.evaluate()
        actual.append(seq2int(simulator.get_value(ShiftRegister.O, scope)))

    assert actual == expected
