from magma import *
import magma as m
from magma.testing.utils import has_error


def test_array_lengths(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array[7, Bit]))

    buf = Buf()
    wire(main.O, buf.I)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:13\033[0m: Cannot wire main.O (type=Array[7, In(Bit)]) to main.buf.I (type=Array[8, In(Bit)]) because the arrays do not have the same length
>>     wire(main.O, buf.I)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


def test_array_to_bit(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:28\033[0m: Cannot wire main.O (type=In(Bit)) to main.buf.I (type=Array[8, In(Bit)]) because main.O is not an Array
>>     wire(main.O, buf.I)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


def test_bit_to_array(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Array[7, Bit]))

    buf = Buf()
    wire(buf.I, main.O)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:43\033[0m: Cannot wire main.buf.I (type=In(Bit)) to main.O (type=Array[7, In(Bit)]) because main.buf.I is not an Array
>>     wire(buf.I, main.O)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


class I(m.Product):
    a = Bit
    b = Bit


def test_tuple_to_array(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(I), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:63\033[0m: Cannot wire main.O (type=In(Bit)) to main.buf.I (type=Tuple(a=In(Bit),b=In(Bit))) because main.O is not a Tuple
>>     wire(main.O, buf.I)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


def test_bad_tuples(caplog):
    m.config.set_debug_mode(True)
    class O(m.Product):
        c = m.In(m.Bit)
        d = m.In(m.Bit)

    Buf = DeclareCircuit('Buf', "I", In(I), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(O))

    buf = Buf()
    wire(main.O, buf.I)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:82\033[0m: Cannot wire main.O (type=Tuple(c=In(Bit),d=In(Bit)), keys=['a', 'b']) to main.buf.I (type=Tuple(a=In(Bit),b=In(Bit)), keys=['c', 'd']) because the tuples do not have the same keys
>>     wire(main.O, buf.I)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


def test_bit_to_array(caplog):
    m.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Array[8, Bit]), "O", Out(Array[8, Bit]))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(buf.I, main.O)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:97\033[0m: Cannot wire main.O (type=In(Bit)) to I (type=Array[8, In(Bit)]) because main.buf.I is not a Digital
>>     wire(buf.I, main.O)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)
