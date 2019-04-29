from magma import *
magma.config.set_debug_mode(True)


def test_input_as_output(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:11: Using `main.O` (an input) as an output
    wire(main.O, buf.I)
"""


def test_output_as_input(caplog):
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a.O)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:24: Using `main.A_inst0.O` (an output) as an input
    wire(main.I, a.O)
"""


def test_multiple_outputs_to_input_warning(caplog):
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits[2]), "O", Out(Bit))

    a = A()
    wire(main.I[0], a.I)
    wire(main.I[1], a.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:38: Adding the output `main.I[1]` to the wire `main.A_inst0.I` which already has output(s) `[main.I[0]]`
    wire(main.I[1], a.I)
"""


def test_muliple_outputs_circuit(caplog):
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = A()
    wire(a, main.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:51: Can only wire circuits with one output. Argument 0 to wire `main.A_inst0` has outputs [inst0.O, inst0.U]
    wire(a, main.I)
"""


def test_muliple_outputs_circuit(caplog):
    A = DeclareCircuit('A', "I", In(Bit), "J", In(Bit), "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    a(main)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:64: Number of inputs is not equal to the number of outputs, expected 2 inputs, got 1. Only 1 will be wired.
    a(main)
"""


def test_no_inputs_circuit(caplog):
    A = DeclareCircuit('A', "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:77: Wiring an output to a circuit with no input arguments, skipping
    wire(main.I, a)
"""


def test_muliple_inputs_circuit(caplog):
    A = DeclareCircuit('A', "I", In(Bit), "J", In(Bit), "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:90: Wiring an output to a circuit with more than one input argument, using the first input main.A_inst0.I
    wire(main.I, a)
"""


def test_no_key(caplog):
    A = DeclareCircuit('A', "I", In(Bit), "J", In(Bit), "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    a(K=main.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:103: Instance main.A_inst0 does not have input K
    a(K=main.I)
"""


def test_const_array_error(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Array[1, Bit]), "O", Out(Array[1, Bit]))

    main = DefineCircuit("main", "O", Out(Array[1, Bit]))

    buf = Buf()

    wire(1, buf.I)
    wire(buf.O, main.O)

    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_wire/test_errors.py:117: Cannot wire 1 (type=<class 'int'>) to main.Buf_inst0.I (type=Array[1, In(Bit)]) because conversions from IntegerTypes are only defined for Bits, not general Arrays
    wire(1, buf.I)
"""
