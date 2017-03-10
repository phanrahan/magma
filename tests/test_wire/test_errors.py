import sys
from magma import *


def test_input_as_output(capsys):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    out, err = capsys.readouterr()
    err_lines = err.splitlines()
    assert err_lines[-1] == "Error: using an input as an output main.O"
    assert err_lines[-2] == "    wire(main.O, buf.I)"


def test_output_as_input(capsys):
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a.O)
    out, err = capsys.readouterr()
    err_lines = err.splitlines()
    assert err_lines[-1] == "Error: using an output as an input inst0.O"
    assert err_lines[-2] == "    wire(main.I, a.O)"
