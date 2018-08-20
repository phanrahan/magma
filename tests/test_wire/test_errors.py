from magma import *


def test_input_as_output(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert caplog.records[-2].msg == "WIRING ERROR: Using an input as an output main.O"
    assert caplog.records[-3].msg == "    wire(main.O, buf.I)"


def test_output_as_input(caplog):
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a.O)
    assert caplog.records[-2].msg == "WIRING ERROR: Using an output as an input inst0.O"
    assert caplog.records[-3].msg == "    wire(main.I, a.O)"


if __name__ == "__main__":
    test_output_as_input(None)
