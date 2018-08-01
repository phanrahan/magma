import magma as m
import mantle


IDLE = m.bits(0, 2)
HBLANK = m.bits(1, 2)
HACT = m.bits(2, 2)

PIX_PER_LINE = m.bits(120, 11)


@m.circuit.combinational
def fsm_logic(current_state: m.Bits(2),
              pixel_count: m.UInt(11),
              frameValid: m.Bit,
              real_href: m.Bit) -> (m.Bits(2), m.UInt(11)):
    """Returns next_state, next_pixel_count"""
    if current_state == IDLE:
        next_state = HBLANK if frameValid else IDLE
        next_pixel_count = m.bits(0, 11)
    elif current_state == HBLANK:
        if real_href:
            next_state = HACT
            next_pixel_count = PIX_PER_LINE
        else:
            next_state = HBLANK
            next_pixel_count = m.bits(0, 11)
    elif current_state == HACT:
        next_state = HBLANK if pixel_count == m.bits(1, 11) else HACT
        # TODO: Support AugAssign node
        # next_pixel_count -= 1
        next_pixel_count = pixel_count - m.uint(1, 11)
    else:
        next_state = IDLE
        next_pixel_count = m.bits(0, 11)
    return next_state, next_pixel_count


class MagmaFSM(m.Circuit):
    IO = ["frameValid", m.In(m.Bit),
          "clk", m.In(m.Clock),
          "rst", m.In(m.AsyncReset),
          "real_href", m.In(m.Bit),
          "pixel_valid", m.Out(m.Bit)]

    @classmethod
    def definition(io):
        state = mantle.Register(2, has_async_reset=True, init=0)
        pixel_count = mantle.Register(11, has_async_reset=True, init=0)

        next_state, next_pixel_count = fsm_logic(
            state.O, m.uint(pixel_count.O), io.frameValid, io.real_href)
        m.wire(next_state, state.I)
        m.wire(next_pixel_count, pixel_count.I)
        m.wire(state.O == HACT, io.pixel_valid)


m.compile("build/MagmaFSM", MagmaFSM, output="coreir-verilog")
