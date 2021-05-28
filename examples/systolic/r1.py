from typing import List

import magma as m


# Actual
def make_R1(width: int, length: int, w: List[int]):
    assert len(w) == length
    T = m.UInt[width]

    # We ignore the extra tag-bit/control required on `w_in` to track when to
    # reset the accum. reg.
    class _Cell(m.Circuit):
        io = m.IO(
            x_in=m.In(T), x_out=m.Out(T),
            w_in=m.In(T), w_out=m.Out(T),
            y_out=m.Out(T))
        io += m.ClockIO()
        io.x_out @= m.register(io.x_in)
        io.w_out @= m.register(io.w_in)
        accum = m.Register(T, init=0)()
        accum.I @= accum.O + io.x_in * io.w_in
        io.y_out @= accum.O
        name = f"R1_cell_{width}"

    # TODO(rsetaluri): Implement this.
    class _OutputCell(m.Circuit):
        name = f"R1_outupt_cell_{width}"
        io = m.IO(I0=m.In(T), I1=m.In(T), O=m.Out(T))

    # We assume the user of this circuit will properly space the `x_in` and
    # `w_in` values by 2 cycles, as well as cycle through the weights.
    class _Top(m.Circuit):
        name = f"R1"
        io = m.IO(x_in=m.In(T), w_in=m.In(T), y_out=m.Out(T))
        io += m.ClockIO()
        cells = [_Cell() for _ in range(length)]
        sys = m.braid(
            cells,
            forkargs=["CLK"],
            foldargs={"x_in": "x_out"}, rfoldargs={"w_in": "w_out"})
        _, _, ys = sys(io.x_in, io.w_in)

        output_cells = [_OutputCell() for _ in range(length)]
        sys_output = m.braid(
            output_cells,
            foldargs={"I0": "O"})
        io.y_out @= sys_output(0, ys)

    return _Top


R1 = make_R1(1, 3, [1, 2, 3])
m.compile(R1.name, R1, inline=True)
