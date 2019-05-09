import magma as m


def test_type_relations():
    class _MyGen(m.Generator):
        pass

    MyCircuit = _MyGen()

    assert issubclass(MyCircuit, m.Circuit)
    assert isinstance(MyCircuit, m.circuit.DefineCircuitKind)
    assert issubclass(m.circuit.Circuit, m.circuit.CircuitType)
    assert issubclass(m.circuit.DefineCircuitKind, m.circuit.CircuitKind)
    assert isinstance(MyCircuit, m.circuit.CircuitKind)

    assert isinstance(MyCircuit, _MyGen)
    assert issubclass(_MyGen, m.circuit.DefineCircuitKind)


def test_generation():
    class _MyGen(m.Generator):
        def new(width):
            io = m.IO(I=m.In(m.Bits[width]),
                      O=m.Out(m.Bits[width]))
            m.wire(io.O, io.I)
            return io

    MyCircuit8 = _MyGen(8)
    print (repr(MyCircuit8))
    m.compile("test", MyCircuit8, output="coreir")
