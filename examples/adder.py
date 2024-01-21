import magma as m
from .full_adder import FullAdder


class Adder(m.Generator):
    """
    n-bit adder with a carry-in and carry-out
    """
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


class Adder2(m.Generator):
    """
    As higher-order circuit
    """
    def __init__(self, n: int):
        self.io = io = m.IO(
            A=m.In(m.UInt[n]),
            B=m.In(m.UInt[n]),
            CIN=m.In(m.Bit),
            SUM=m.Out(m.UInt[n]),
            COUT=m.Out(m.Bit)
        )
        cout, _sum = m.braid(
            (FullAdder() for _ in range(n)),
            joinargs=["A", "B", "C"],
            foldargs={"cin": "cout"}
        )(io.A, io.B, io.CIN)
        io.SUM @= _sum
        io.COUT @= cout
