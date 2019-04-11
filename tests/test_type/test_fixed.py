import magma as m
from magma.testing import check_files_equal


def test_sfixed_simple():
    x = m.SFixed[25, 2]
    assert x.W == 25
    assert x.I == 2
    xi = m.In(x)
    xo = m.Out(x)
    assert xi.T.isinput()
    assert xo.T.isoutput()


def test_sfixed_mul():
    T_u = m.SFixed[18, -2]
    T_x = m.SFixed[25, 2]
    out_width = T_u.W + T_x.W
    T_o = m.SFixed[out_width, T_u.I + T_x.I]
    class MulFixed(m.Circuit):
        IO = ["u", m.In(T_u), "x", m.In(T_x), "o", m.Out(T_o)]
        @classmethod
        def definition(io):
            coreir_io = ['in0', m.In(T_o), 'in1', m.In(T_o), 'out', m.Out(T_o)]
            CoreIRMul = m.DeclareCircuit("coreir_mul", *coreir_io,
                                         coreir_name="mul", coreir_lib="coreir",
                                         coreir_genargs={"width": out_width})
            io.o <= CoreIRMul()(m.sext(io.u, out_width - T_u.W),
                                m.sext(io.x, out_width - T_x.W))
    m.compile("build/test_mul_fixed", MulFixed, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/test_mul_fixed.v",
                             f"gold/test_mul_fixed.v")


