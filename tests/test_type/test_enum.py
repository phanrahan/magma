import magma as m
from magma.testing import check_files_equal


def test_enum():
    State = m.Enum(
        zero=0,
        one=1,
        two=2
    )
    circuit = m.DefineCircuit('enum_test', "I", m.In(State), "O", m.Out(m.Array(2, State)))
    m.wire(circuit.I, circuit.O[0])
    m.wire(State.zero, circuit.O[1])
    m.EndDefine()
    m.compile("build/test_enum", circuit, output="coreir-verilog")
    check_files_equal(__file__, "build/test_enum.v", "gold/test_enum.v")
