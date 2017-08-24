from magma import *


def test_input_as_output(capsys):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    out, err = capsys.readouterr()
    err_lines = err.splitlines()
    assert err_lines[-1] == "=" * 80
    assert err_lines[-2] == "Error: using an input as an output O"
    assert err_lines[-3] == "    wire(main.O, buf.I)"


def test_output_as_input(capsys):
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a.O)
    out, err = capsys.readouterr()
    err_lines = err.splitlines()
    assert err_lines[-1] == "=" * 80
    assert err_lines[-2] == "Error: using an output as an input O"
    assert err_lines[-3] == "    wire(main.I, a.O)"

