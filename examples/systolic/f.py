from typing import List

import magma as m


# Actual
def make_F(width: int, length: int, w: List[int]):
    assert len(w) == length
    T = m.UInt[width]

    class _Cell(m.Generator2):
        def __init__(self, w: int):
            self.io = m.IO(x_in=m.In(T), x_out=m.Out(T), z_out=m.Out(T))
            self.io += m.ClockIO()
            self.io.x_out @= m.register(self.io.x_in)
            self.io.z_out @= w * self.io.x_in
            self.name = f"F_cell_{width}_{w}"

    class _Top(m.Circuit):
        name = f"F"
        io = m.IO(x_in=m.In(T), y_out=m.Out(T))
        io += m.ClockIO()
        cells = [_Cell(wi)() for wi in w]
        sys = m.braid(cells, forkargs=["CLK"], foldargs={"x_in": "x_out"})
        _, zs = sys(io.x_in)
        io.y_out @= sum(zs[1:], zs[0])

    return _Top


F = make_F(4, 3, [0, 0, 0])
m.compile(F.name, F, inline=True)
