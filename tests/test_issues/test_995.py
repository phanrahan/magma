import dataclasses
import functools

import magma as m
from magma.testing import check_files_equal


def test_995():
    IDLE, CALC, DONE = 0, 1, 2

    A_MUX_SEL_IN    = m.bits(0, 2)
    A_MUX_SEL_SUB   = m.bits(1, 2)
    A_MUX_SEL_B     = m.bits(2, 2)
    A_MUX_SEL_X     = m.bits(0, 2)

    B_MUX_SEL_A     = m.bits(0, 1)
    B_MUX_SEL_IN    = m.bits(1, 1)
    B_MUX_SEL_X     = m.bits(0, 1)

    def f0(a, b):
        return a - b, a < b, b == 0

    def f1(resp_msg, a_in, b_in, a_reg, b_reg, a_mux_sel, b_mux_sel):
        a_next = m.mux([a_in, resp_msg, b_reg], a_mux_sel)
        b_next = m.mux([a_reg, b_in], b_mux_sel)
        return a_next, b_next

    @m.combinational2()
    def f3(curr: m.Bits[2], is_b_zero: m.Bit,
           is_a_lt_b: m.Bit) -> m.Tuple[m.Bit, m.Bit, m.Bits[2], m.Bit,
                                        m.Bits[1], m.Bit]:
        if curr == IDLE:
            req_rdy   = m.Bit(1)
            resp_val  = m.Bit(0)
            a_mux_sel = A_MUX_SEL_IN
            a_reg_en  = m.Bit(1)
            b_mux_sel = B_MUX_SEL_IN
            b_reg_en  = m.Bit(1)
        elif curr == CALC:
            do_swap = is_a_lt_b
            do_sub  = ~is_b_zero
            req_rdy   = m.Bit(0)
            resp_val  = m.Bit(0)
            if do_swap:
                a_mux_sel = A_MUX_SEL_B
            else:
                a_mux_sel = A_MUX_SEL_SUB
            a_reg_en  = m.Bit(1)
            b_mux_sel = B_MUX_SEL_A
            b_reg_en  = do_swap
        elif curr == DONE:
            req_rdy   = m.Bit(0)
            resp_val  = m.Bit(1)
            a_mux_sel = A_MUX_SEL_X
            a_reg_en  = m.Bit(0)
            b_mux_sel = B_MUX_SEL_X
            b_reg_en  = m.Bit(0)
        return m.tuple_([req_rdy, resp_val, a_mux_sel, a_reg_en, b_mux_sel, b_reg_en])

    class Gcd(m.Generator2):
        def __init__(self, width: int):
            ReqT = m.Product.from_fields(
                "Req", dict(
                    msg=m.In(m.Bits[width * 2]),
                    rdy=m.Out(m.Bit),
                    val=m.In(m.Bit)))
            RespT = m.Product.from_fields(
                "Resp", dict(
                    msg=m.Out(m.Bits[width]),
                    rdy=m.In(m.Bit),
                    val=m.Out(m.Bit)))
            self.io = io = m.IO(
                clk=m.In(m.Clock),
                reset=m.In(m.Reset),
                req=ReqT,
                resp=RespT,
            )
            self.name = f"Gcd{width}"

            a_in = m.uint(io.req.msg[:width])
            b_in = m.uint(io.req.msg[width:])

            a_reg = m.Register(m.UInt[width], has_enable=True)(name="a_reg")
            b_reg = m.Register(m.UInt[width], has_enable=True)(name="b_reg")
            state = m.Register(m.Bits[2])(name="state")

            curr = state.O
            next = m.Bits[2](name="next")

            resp_msg, is_a_lt_b, is_b_zero = f0(a_reg.O, b_reg.O)

            (req_rdy, resp_val, a_mux_sel,
             a_reg_en, b_mux_sel, b_reg_en) = f3(curr, is_b_zero, is_a_lt_b)

            a_next, b_next = f1(resp_msg, a_in, b_in, a_reg.O, b_reg.O,
                                a_mux_sel, b_mux_sel)

            a_reg.CE @= m.Enable(a_reg_en)
            b_reg.CE @= m.Enable(b_reg_en)

            @m.inline_combinational()
            def _():
                next @= curr
                if curr == IDLE:
                    if io.req.val and req_rdy:
                        next @= CALC
                elif curr == CALC:
                    if not is_a_lt_b and is_b_zero:
                        next @= DONE
                elif curr == DONE:
                    if resp_val and io.resp.rdy:
                        next @= IDLE

            state.I @= next

            a_reg.I @= a_next
            b_reg.I @= b_next

            io.resp.val @= resp_val
            io.req.rdy @= req_rdy
            io.resp.msg @= resp_msg

    width = 16
    ckt = Gcd(width)
    m.compile("build/test_995", ckt, inline=True)
    assert check_files_equal(__file__, f"build/test_995.v", f"gold/test_995.v")
