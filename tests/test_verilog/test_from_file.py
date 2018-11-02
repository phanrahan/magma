import magma as m
import magma.testing
import os

def check_port(definition, port, type, direction):
    assert hasattr(definition, port)
    port = getattr(definition, port)
    assert isinstance(port, type)
    if direction == "input":
        assert port.isoutput()
    elif direction == "output":
        assert port.isinput()
    else:
        raise NotImplementedError(direction)

def check_rxmod(RXMOD):
    check_port(RXMOD, "RX", m.BitType, "input")
    check_port(RXMOD, "CLK", m.BitType, "input")
    check_port(RXMOD, "data", m.ArrayType, "output")
    check_port(RXMOD, "valid", m.BitType, "output")

    m.compile("build/test_rxmod", RXMOD)
    assert m.testing.check_files_equal(__file__, "build/test_rxmod.v",
            "gold/test_rxmod.v")    

def test_basic():
    file_path = os.path.dirname(__file__)
    RXMOD = m.DefineFromVerilogFile(os.path.join(file_path, "rxmod.v"))[0]

    check_rxmod(RXMOD)


def test_target_modules_arg():
    file_path = os.path.dirname(__file__)
    circuits = m.DefineFromVerilogFile(os.path.join(file_path, "rxmod.v"), ["RXMOD"])
    assert len(circuits) == 1
    assert circuits[0].name == "RXMOD"

    check_rxmod(circuits[0])
