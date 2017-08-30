
from magma import *
from magma.primitives import DefineRegister

from magma.simulator import PythonSimulator
from magma.scope import Scope
from magma.bit_vector import BitVector
from magma.bitutils import int2seq, seq2int

def test_instance():
    N = 4
    Register4 = DefineRegister(4)
    T = Bits(N)

    class ShiftRegister(Circuit):
        name = "ShiftRegister"
        IO = ["I", In(T), "O", Out(T), "CLK", In(Bit)]
        @classmethod
        def definition(io):
            regs = [Register4() for _ in range(N)]
            wireclock(io, regs)
            wire(io.I, getattr(regs[0], "in"))
            fold(regs, foldargs={"in":"out"})
            wire(regs[-1].out, io.O)

    try:
        simulator = PythonSimulator(ShiftRegister())
        assert False, "Should raise a ValueError when passing an instance to the Python Simulator"
    except ValueError as e:
        pass
