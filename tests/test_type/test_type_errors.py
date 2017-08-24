from magma import *


def test_array_lengths(capsys):
    Buf = DeclareCircuit('Buf', "I", In(Array(8, Bit)), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array(7, Bit)))

    buf = Buf()
    wire(main.O, buf.I)
    out, err = capsys.readouterr()
    err_lines = err.splitlines()
    assert err_lines[-1] == "=" * 80
    assert err_lines[-2] == "Wiring Error: Arrays must have the same length 8 != 7"
    assert err_lines[-3] == "    wire(main.O, buf.I)"


def test_array_to_bit(capsys):
    Buf = DeclareCircuit('Buf', "I", In(Array(8, Bit)), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    out, err = capsys.readouterr()
    err_lines = err.splitlines()
    assert err_lines[-1] == "=" * 80
    assert err_lines[-2] == "Wiring Error: wiring O (In(Bit)) to I (Array(8,In(Bit)))"
    assert err_lines[-3] == "    wire(main.O, buf.I)"

def test_bit_to_array(capsys):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array(7, Bit)))

    buf = Buf()
    wire(buf.I, main.O)
    out, err = capsys.readouterr()
    err_lines = err.splitlines()
    assert err_lines[-1] == "=" * 80
    assert err_lines[-2] == "Wiring Error: wiring I (In(Bit)) to O (Array(7,In(Bit)))"
    assert err_lines[-3] == "    wire(buf.I, main.O)"
