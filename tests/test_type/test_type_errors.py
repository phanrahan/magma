from magma import *


def test_array_lengths(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Array(8, Bit)), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array(7, Bit)))

    buf = Buf()
    wire(main.O, buf.I)
    assert caplog.records[-2].msg == "Wiring Error: Arrays must have the same length 8 != 7"
    assert caplog.records[-3].msg == "    wire(main.O, buf.I)"


def test_array_to_bit(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Array(8, Bit)), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert caplog.records[-2].msg == "Wiring Error: wiring main.O (In(Bit)) to inst0.I (Array(8,In(Bit)))"
    assert caplog.records[-3].msg == "    wire(main.O, buf.I)"

def test_bit_to_array(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array(7, Bit)))

    buf = Buf()
    wire(buf.I, main.O)
    assert caplog.records[-2].msg == "Wiring Error: wiring inst0.I (In(Bit)) to main.O (Array(7,In(Bit)))"
    assert caplog.records[-3].msg == "    wire(buf.I, main.O)"
