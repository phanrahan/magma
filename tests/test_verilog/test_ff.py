import magma as m
import magma.testing
import os
import pytest


@pytest.mark.parametrize("target", ["verilog", "coreir", "coreir-verilog"])
@pytest.mark.parametrize("circuit_type", ["declare", "define"])
def test_ff_param(target, circuit_type):
    suffix = {
        "verilog": "v",
        "coreir": "json",
        "coreir-verilog": "v"
    }[target]

    constructor = {
        "declare": m.declare_from_verilog_file,
        "define": m.define_from_verilog_file
    }[circuit_type]

    ff_file = os.path.join(os.path.dirname(__file__), "ff.v")

    FF = constructor(
        ff_file,
        type_map={"clk": m.In(m.Clock), "rst": m.In(m.AsyncReset)}
    )[0]

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[2])) + \
            m.ClockIO(has_async_reset=True)

        # keyword arguments to instancing call are passed as verilog
        # parameters
        ff0 = FF(init=0)
        ff1 = FF(init=1)
        io.O <= m.join([ff0, ff1])(d=io.I, rst=io.ASYNCRESET)

    m.compile(f"build/top-{circuit_type}-{target}", Top, output=target)
    assert m.testing.check_files_equal(__file__,
                                       f"build/top-{circuit_type}-{target}.{suffix}",
                                       f"gold/top-{circuit_type}-{target}.{suffix}")
