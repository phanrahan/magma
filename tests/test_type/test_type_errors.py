from magma import *


def test_array_lengths(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Array(8, Bit)), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array(7, Bit)))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:10: Cannot wire main.O (type=Array(7,In(Bit)), len=8) to inst0.I (type=Array(8,In(Bit)), len=7) because the arrays do not have the same length
    wire(main.O, buf.I)
"""


def test_array_to_bit(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Array(8, Bit)), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:23: Cannot wire main.O (type=In(Bit)) to inst0.I (type=Array(8,In(Bit))) because main.O is not an Array
    wire(main.O, buf.I)
"""


def test_bit_to_array(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Array(8, Bit)))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array(7, Bit)))

    buf = Buf()
    wire(buf.I, main.O)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:36: Cannot wire inst0.I (type=In(Bit)) to main.O (type=Array(7,In(Bit))) because inst0.I is not an Array
    wire(buf.I, main.O)
"""
