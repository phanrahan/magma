from magma import *
m.config.set_debug_mode(True)


def test_array_lengths(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array[7, Bit]))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:11: Cannot wire main.O (type=Array[7, In(Bit)]) to main.Buf_inst0.I (type=Array[8, In(Bit)]) because the arrays do not have the same length
    wire(main.O, buf.I)
"""


def test_array_to_bit(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:24: Cannot wire main.O (type=In(Bit)) to main.Buf_inst0.I (type=Array[8, In(Bit)]) because main.O is not an Array
    wire(main.O, buf.I)
"""


def test_bit_to_array(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array[7, Bit]))

    buf = Buf()
    wire(buf.I, main.O)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:37: Cannot wire main.Buf_inst0.I (type=In(Bit)) to main.O (type=Array[7, In(Bit)]) because main.Buf_inst0.I is not an Array
    wire(buf.I, main.O)
"""


class I(m.Product):
    a = Bit
    b = Bit


def test_tuple_to_array(caplog):
    Buf = DeclareCircuit('Buf', "I", In(I), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:55: Cannot wire main.O (type=In(Bit)) to main.Buf_inst0.I (type=Tuple(a=In(Bit),b=In(Bit))) because main.O is not a Tuple
    wire(main.O, buf.I)
"""


def test_bad_tuples(caplog):
    class O(m.Product):
        c = m.In(m.Bit)
        d = m.In(m.Bit)

    Buf = DeclareCircuit('Buf', "I", In(I), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(O))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:72: Cannot wire main.O (type=Tuple(c=In(Bit),d=In(Bit)), keys=['a', 'b']) to main.Buf_inst0.I (type=Tuple(a=In(Bit),b=In(Bit)), keys=['c', 'd']) because the tuples do not have the same keys
    wire(main.O, buf.I)
"""


def test_bit_to_array(caplog):
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(buf.I, main.O)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:85: Cannot wire main.O (type=In(Bit)) to I (type=Array[8, In(Bit)]) because main.Buf_inst0.I is not a Digital
    wire(buf.I, main.O)
"""
