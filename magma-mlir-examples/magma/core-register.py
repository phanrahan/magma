import magma as m

from common import print_verilog


if __name__ == "__main__":
    T = m.Bits[8]
    opts = dict(init=0, reset_type=m.Reset, has_enable=True)
    ckt = m.Register(T, **opts)
    print_verilog(ckt, inline=True, passes=["rungenerators", "inline_single_instances", "clock_gate"])
