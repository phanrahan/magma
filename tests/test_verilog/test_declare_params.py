import magma as m
import magma.testing


def test_declare_FF_with_params():
    FF = m.DeclareCircuit("FF",
                          "I", m.In(m.Bit),
                          "O", m.Out(m.Bit),
                          "CLK", m.In(m.Clock))
    FF.coreir_config_param_types = {
        "init": int
    }

    class Top(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit), "CLK", m.In(m.Clock)]
        @classmethod
        def definition(io):
            ff0 = FF(init=0)
            ff1 = FF(init=1)
            io.O <= m.fold(ff0, ff1)(io.I)

    m.compile("build/Top", Top, output="coreir-verilog")
    assert m.testing.check_files_equal(__file__,
                                       f"build/Top.v",
                                       f"gold/Top.v")
