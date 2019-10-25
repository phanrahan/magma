from magma import *
import magma as m


def test_array_lengths(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array[7, Bit]))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:12: Cannot wire main.O (type=Array[7, In(Bit)]) to main.buf.I (type=Array[8, In(Bit)]) because the arrays do not have the same length
    wire(main.O, buf.I)
"""
    m.config.set_debug_mode(False)


def test_array_to_bit(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:27: Cannot wire main.O (type=In(Bit)) to main.buf.I (type=Array[8, In(Bit)]) because main.O is not an Array
    wire(main.O, buf.I)
"""
    m.config.set_debug_mode(False)


def test_bit_to_array(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array[7, Bit]))

    buf = Buf()
    wire(buf.I, main.O)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:36: Cannot wire main.buf.I (type=In(Bit)) to main.O (type=Array[7, In(Bit)]) because main.buf.I is not an Array
    wire(buf.I, main.O)
"""
    m.config.set_debug_mode(False)


def test_tuple_to_array(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Tuple(a=Bit,b=Bit)), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:57: Cannot wire main.O (type=In(Bit)) to main.buf.I (type=Tuple(a=In(Bit),b=In(Bit))) because main.O is not a Tuple
    wire(main.O, buf.I)
"""
    m.config.set_debug_mode(False)


def test_bad_tuples(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Tuple(a=Bit,b=Bit)), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Tuple(c=Bit,d=Bit)))

    buf = Buf()
    wire(main.O, buf.I)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:72: Cannot wire main.O (type=Tuple(c=In(Bit),d=In(Bit)), keys=['a', 'b']) to main.buf.I (type=Tuple(a=In(Bit),b=In(Bit)), keys=['c', 'd']) because the tuples do not have the same keys
    wire(main.O, buf.I)
"""
    m.config.set_debug_mode(False)


def test_bit_to_array(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(buf.I, main.O)
    assert "\n".join(x.msg for x in caplog.records) == """\
\033[1mtests/test_type/test_type_errors.py:87: Cannot wire main.O (type=In(Bit)) to I (type=Array[8, In(Bit)]) because main.buf.I is not a _Bit
    wire(buf.I, main.O)
"""
    m.config.set_debug_mode(False)
