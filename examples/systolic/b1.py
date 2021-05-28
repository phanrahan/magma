from typing import List

import magma as m


# Ideal
def make_B1(length: int):
    return braid(
        [lambda x_in, y_in: y_in + x_in * w[i] for i in range(length)],
        fork_args=["x_in"],
        fold_args={"y_in": "y_out"})


# Actual
def make_B1(width: int, length: int, w: List[int]):
    assert len(w) == length
    T = m.UInt[width]

    class _Cell(m.Generator2):
        def __init__(self, w: int):
            self.io = m.IO(x_in=m.In(T), y_in=m.In(T), y_out=m.Out(T))
            self.io += m.ClockIO()
            self.io.y_out @= m.register(self.io.y_in + self.io.x_in * w, init=0)
            self.name = f"B1_cell_{width}_{w}"

    class _Top(m.Circuit):
        name = f"B1"
        io = m.IO(x_in=m.In(T), y_out=m.Out(T))
        io += m.ClockIO()
        cells = [_Cell(w[i])() for i in range(length)]
        sys = m.braid(
            cells,
            forkargs=["x_in", "CLK"],
            foldargs={"y_in": "y_out"})
        io.y_out @= sys(io.x_in, 0)

    return _Top


B1 = make_B1(4, 3, [1, 2, 3])
m.compile(B1.name, B1, inline=True)
