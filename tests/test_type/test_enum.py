import pytest
import magma as m
from magma.testing import check_files_equal


def test_enum():
    class State(m.Enum):
        zero = 0
        one = 1
        two = 2

    assert issubclass(State, m.Enum)

    class circuit(m.Circuit):
        name = "enum_test"
        io = m.IO(I=m.In(State),
                  O=m.Out(m.Array[2, State]))
        m.wire(io.I, io.O[0])
        m.wire(State.zero, io.O[1])
    m.compile("build/test_enum", circuit, output="coreir-verilog")
    assert check_files_equal(__file__, "build/test_enum.v", "gold/test_enum.v")


def test_enum_max_value():
    class State(m.Enum):
        zero = 0
        one = 1
        four = 4

    class circuit(m.Circuit):
        name = "enum_test_max_value"
        io = m.IO(I=m.In(State),
                  O=m.Out(m.Array[2, State]))
        m.wire(io.I, io.O[0])
        m.wire(State.four, io.O[1])
    m.compile("build/test_enum_max_value", circuit, output="coreir-verilog")
    assert check_files_equal(__file__, "build/test_enum_max_value.v",
                             "gold/test_enum_max_value.v")


def test_reserved():
    with pytest.raises(ValueError):
        class MyEnum(m.Enum):
            a = 0
            N = 2
