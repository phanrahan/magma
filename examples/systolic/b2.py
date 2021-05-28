from typing import List

import magma as m


# Actual
def make_B2(width: int, length: int, w: List[int]):
    assert len(w) == length
    T = m.UInt[width]

    # We ignore the extra tag-bit/control required on `w_in` to track when to
    # reset the accum. reg.
    class _Cell(m.Generator2):
        def __init__(self, w: int):
            self.io = m.IO(x_in=m.In(T), w_in=m.In(T), w_out=m.Out(T), y_out=m.Out(T))
            self.io += m.ClockIO()
            accum = m.Register(T, init=0)()
            # NOTE(rsetaluri): We initialize the `w` pipeline reg's with `w`.
            self.io.w_out @= m.register(self.io.w_in, init=w)
            accum.I @= accum.O + self.io.x_in * self.io.w_in
            self.io.y_out @= accum.O
            self.name = f"B2_cell_{width}_{w}"

    class _Top(m.Circuit):
        name = f"B2"
        # Ignores control; just outputs y's.
        io = m.IO(x_in=m.In(T), y_out=m.Out(m.Array[length, T]))
        io += m.ClockIO()
        cells = [_Cell(wi)() for wi in w]
        sys = m.braid(cells, forkargs=["x_in", "CLK"], foldargs={"w_in": "w_out"})
        # Temporary needed for loop.
        w_in = T()
        w_out, y_out = sys(io.x_in, w_in)
        w_in @= w_out
        io.y_out @= y_out

    return _Top


B2 = make_B2(4, 3, [1, 2, 3])
m.compile(B2.name, B2, inline=True)
