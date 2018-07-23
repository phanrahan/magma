import magma as m
from magma.operators import MantleImportError


def test_error():
    circ = m.DefineCircuit("test", "a", m.In(m.Bits(4)), "b", m.Out(m.Bits(4)))
    try:
        ~circ.a
        assert False, \
            "Operator should throw an error since mantle is not imported"
    except MantleImportError:
        pass
