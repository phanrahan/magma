from magma import *


def test_input_as_output(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:10: Using main.O (an input) as an output
    wire(main.O, buf.I)
"""


def test_output_as_input(caplog):
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a.O)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:23: Using main.A_inst0.O (an output) as an input
    wire(main.I, a.O)
"""


if __name__ == "__main__":
    test_output_as_input(None)
