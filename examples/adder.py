import magma as m
from .full_adder import FullAdder


# n-bit adder with carry in and carry out
class Adder(m.Generator):
    def __init__(self, n: int):
        self.io = io = m.IO(
            A=m.In(m.UInt[n]),
            B=m.In(m.UInt[n]),
            CIN=m.In(m.Bit),
            SUM=m.Out(m.UInt[n]),
            COUT=m.Out(m.Bit)
        )
        curr_cin = io.CIN
        for i in range(n):
            next_sum, curr_cin = FullAdder()(io.A[i], io.B[i], curr_cin)
            io.SUM[i] @= next_sum
        io.COUT @= curr_cin
