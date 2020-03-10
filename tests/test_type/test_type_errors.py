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
\033[1mtests/test_type/test_type_errors.py:16\033[0m: Cannot wire .O (type=Array[7, In(Bit)]) to ..I (type=Array[8, In(Bit)]) because the arrays do not have the same length
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
\033[1mtests/test_type/test_type_errors.py:34\033[0m: Cannot wire .O (type=In(Bit)) to ..I (type=Array[8, In(Bit)]) because .O is not an Array
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
\033[1mtests/test_type/test_type_errors.py:51\033[0m: Cannot wire ..I (type=In(Bit)) to .O (type=Array[7, In(Bit)]) because ..I is not an Array
>>         wire(buf.I, .O)"""
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
\033[1mtests/test_type/test_type_errors.py:75\033[0m: Cannot wire .O (type=In(Bit)) to ..I (type=Tuple(a=In(Bit),b=In(Bit))) because .O is not a Tuple
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
\033[1mtests/test_type/test_type_errors.py:97\033[0m: Cannot wire .O (type=Tuple(c=In(Bit),d=In(Bit)), keys=['a', 'b']) to ..I (type=Tuple(a=In(Bit),b=In(Bit)), keys=['c', 'd']) because the tuples do not have the same keys
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
\033[1mtests/test_type/test_type_errors.py:115\033[0m: Cannot wire .O (type=In(Bit)) to I (type=Array[8, In(Bit)]) because ..I is not a Digital
>>         wire(buf.I, io.O)"""
    assert has_error(caplog, msg)
    m.config.set_debug_mode(False)
