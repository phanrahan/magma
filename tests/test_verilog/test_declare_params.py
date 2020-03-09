import magma as m
import magma.testing


def test_declare_FF_with_params():

    class _FF(m.Circuit):
        name = "FF"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit), CLK=m.In(m.Clock))

    _FF.coreir_config_param_types = {"init": int}

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit), CLK=m.In(m.Clock))
        ff0 = _FF(init=0)
        ff1 = _FF(init=1)
        io.O <= m.fold(ff0, ff1)(io.I)

    m.compile("build/Top", Top, output="coreir-verilog")
    assert m.testing.check_files_equal(__file__,
                                       f"build/Top.v",
                                       f"gold/Top.v")
