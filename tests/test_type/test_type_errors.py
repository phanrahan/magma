from magma import *
import magma as m
from magma.testing.utils import has_error


def test_array_lengths(caplog):
    m.config.set_debug_mode(True)
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Array[8, Bit]), O=Out(Array[8, Bit]))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Array[7, Bit]))
        buf = Buf()
        wire(io.O, buf.I)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:16\033[0m: Cannot wire main.O (Array[(7, In(Bit))]) to main.buf.I (Array[(8, In(Bit))])
>>         wire(io.O, buf.I)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


def test_array_to_bit(caplog):
    m.config.set_debug_mode(True)
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Array[8, Bit]), O=Out(Array[8, Bit]))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        buf = Buf()
        wire(io.O, buf.I)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:34\033[0m: Cannot wire main.O (In(Bit)) to main.buf.I (Array[(8, In(Bit))])
>>         wire(io.O, buf.I)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


def test_bit_to_array(caplog):
    m.config.set_debug_mode(True)
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Array[8, Bit]))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Array[7, Bit]))
        buf = Buf()
        wire(buf.I, io.O)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:51\033[0m: Cannot wire main.buf.I (type=In(Bit)) to main.O (type=Array[7, In(Bit)]) because main.buf.I is not an Array
>>         wire(buf.I, main.O)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


class I(m.Product):
    a = Bit
    b = Bit


def test_tuple_to_array(caplog):
    m.config.set_debug_mode(True)
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(I), O=Out(Array[8, Bit]))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        buf = Buf()
        wire(io.O, buf.I)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:75\033[0m: Cannot wire main.O (In(Bit)) to main.buf.I (Tuple(a=In(Bit),b=In(Bit)))
>>         wire(io.O, buf.I)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


def test_bad_tuples(caplog):
    m.config.set_debug_mode(True)
    class O(m.Product):
        c = m.In(m.Bit)
        d = m.In(m.Bit)

    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(I), O=Out(Array[8, Bit]))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(O))
        buf = Buf()
        wire(io.O, buf.I)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:97\033[0m: Cannot wire main.O (Tuple(c=In(Bit),d=In(Bit))) to main.buf.I (Tuple(a=In(Bit),b=In(Bit)))
>>         wire(io.O, buf.I)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)


def test_bit_to_array(caplog):
    m.config.set_debug_mode(True)
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Array[8, Bit]), O=Out(Array[8, Bit]))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        buf = Buf()
        wire(buf.I, io.O)
    msg = """\
\033[1mtests/test_type/test_type_errors.py:115\033[0m: Cannot wire main.buf.I (Array[(8, In(Bit))]) to main.O (In(Bit))
>>         wire(buf.I, io.O)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)
