import pytest
from itertools import product
from collections import OrderedDict
from magma import \
    GND, VCC, \
    bit, Bit, \
    clock, Clock, \
    reset, Reset, \
    enable, Enable, \
    array, Array, \
    bits, Bits, \
    uint, UInt, \
    sint, SInt, \
    zext, sext, \
    tuple_, Tuple, \
    namedtuple, Product
from magma.bitutils import seq2int
import magma as m

def test_bit():
    class Foo(m.Circuit):
        assert isinstance(bit(0), Bit)
        assert isinstance(bit(1), Bit)
        assert isinstance(bit(VCC), Bit)
        assert isinstance(bit(GND), Bit)
        assert isinstance(bit(bit(0)), Bit)
        assert isinstance(bit(clock(0)), Bit)
        assert isinstance(bit(reset(0)), Bit)
        assert isinstance(bit(enable(0)), Bit)
        assert isinstance(bit(bits(0,1)), Bit)
        assert isinstance(bit(uint(0,1)), Bit)
        assert isinstance(bit(sint(0,1)), Bit)

def test_enable():
    class Foo(m.Circuit):
        assert isinstance(enable(0), Enable)
        assert isinstance(enable(1), Enable)
        assert isinstance(enable(VCC), Enable)
        assert isinstance(enable(GND), Enable)
        assert isinstance(enable(bit(0)), Enable)
        assert isinstance(enable(clock(0)), Enable)
        assert isinstance(enable(reset(0)), Enable)
        assert isinstance(enable(enable(0)), Enable)
        assert isinstance(enable(bits(0,1)), Enable)
        assert isinstance(enable(uint(0,1)), Enable)
        assert isinstance(enable(sint(0,1)), Enable)

def test_reset():
    class Foo(m.Circuit):
        assert isinstance(reset(0), Reset)
        assert isinstance(reset(1), Reset)
        assert isinstance(reset(VCC), Reset)
        assert isinstance(reset(GND), Reset)
        assert isinstance(reset(bit(0)), Reset)
        assert isinstance(reset(clock(0)), Reset)
        assert isinstance(reset(enable(0)), Reset)
        assert isinstance(reset(reset(0)), Reset)
        assert isinstance(reset(bits(0,1)), Reset)
        assert isinstance(reset(uint(0,1)), Reset)
        assert isinstance(reset(sint(0,1)), Reset)

def test_clock():
    class Foo(m.Circuit):
        assert isinstance(clock(0), Clock)
        assert isinstance(clock(1), Clock)
        assert isinstance(clock(VCC), Clock)
        assert isinstance(clock(GND), Clock)
        assert isinstance(clock(bit(0)), Clock)
        assert isinstance(clock(clock(0)), Clock)
        assert isinstance(clock(reset(0)), Clock)
        assert isinstance(clock(enable(0)), Clock)
        assert isinstance(clock(bits(0,1)), Clock)
        assert isinstance(clock(uint(0,1)), Clock)
        assert isinstance(clock(sint(0,1)), Clock)

def test_array():
    class Foo(m.Circuit):
        assert isinstance(array(1,4), Array)
        assert isinstance(array([1,0,0,0]), Array)
        assert isinstance(array(VCC), Array)
        assert isinstance(array(array(1,4)), Array)
        assert isinstance(array(uint(1,4)), Array)
        assert isinstance(array(sint(1,4)), Array)

def test_bits():
    class Foo(m.Circuit):
        assert isinstance(bits(1,4), Bits)
        assert isinstance(bits([1,0,0,0]), Bits)
        assert isinstance(bits(VCC), Bits)
        assert isinstance(bits(array(1,4)), Bits)
        assert isinstance(bits(uint(1,4)), Bits)
        assert isinstance(bits(sint(1,4)), Bits)

def test_uint():
    class Foo(m.Circuit):
        assert isinstance(uint(1,4), UInt)
        assert isinstance(uint([1,0,0,0]), UInt)
        assert isinstance(uint(VCC), UInt)
        assert isinstance(uint(array(1,4)), UInt)
        assert isinstance(uint(bits(1,4)), UInt)
        #assert isinstance(uint(sint(1,4)), UInt)

def test_sint():
    class Foo(m.Circuit):
        assert isinstance(sint(1,4), SInt)
        assert isinstance(sint([1,0,0,0]), SInt)
        assert isinstance(sint(VCC), SInt)
        assert isinstance(sint(array(1,4)), SInt)
        assert isinstance(sint(bits(1,4)), SInt)
        #assert isinstance(sint(sint(1,4)), SInt)


def test_tuple_product():
    class Foo(m.Circuit):
        assert isinstance(namedtuple(x=False, y=True), Product)
        assert isinstance(tuple_([0,1]), Tuple)
        assert isinstance(tuple_(VCC), Tuple)
        assert isinstance(tuple_(array(1,4)), Tuple)
        assert isinstance(tuple_(bits(1,4)), Tuple)
        assert isinstance(tuple_(sint(1,4)), Tuple)
        assert isinstance(tuple_(uint(1,4)), Tuple)


@pytest.mark.parametrize("type_,value",
                         product([bits, sint, uint], [-5, 0, 10]))
def test_zext(type_, value):
    if type_ != sint:
        value = abs(value)

    class Foo(m.Circuit):
        in_ = type_(value, 16)
        out = zext(in_, 16)
        assert len(out.bits()) == 32
        # If we have a negative number, then zext should not return the same (signed
        # value). It will instead return the unsigned interpretation of the original
        # bits.
        if value < 0:
            assert int(out) == seq2int(in_.bits())
        else:
            assert int(out) == value


@pytest.mark.parametrize("value", [-5, 0, 10])
def test_sext(value):
    class Foo(m.Circuit):
        in_ = sint(value, 16)
        # TODO(rsetaluri): Ideally, zext(sint) should return an object of type
        # SintType, instead it returns an object of type Array. For now, we wrap
        # the result of zext() in sint().
        out = sint(sext(in_, 16))
        assert len(out.bits()) == 32
        assert int(out) == value


@pytest.mark.skip("Check removed so anonymous bits can be extended")
@pytest.mark.parametrize("op", [m.zext, m.sext])
def test_extension_error(op):
    try:
        class Foo(m.Circuit):
            a = m.In(m.SInt[2])()
            op(a, 2)
        assert False, "This should raise an exception"
    except Exception as e:
        assert str(e) == f"{op.__name__} only works with non input values"


@pytest.mark.parametrize("op", [m.zext, m.sext])
def test_extension_no_error(op):
    try:
        class Foo(m.Circuit):
            a = m.Out(m.SInt[2])()
            op(a, 2)
    except Exception as e:
        assert False, "This should work"


def test_bits_of_bit():
    class Foo(m.Circuit):
        assert repr(m.bits(m.Bit(1), 2)) == "Bits[2](1)"


def test_uint_of_bit():
    class Foo(m.Circuit):
        assert repr(m.uint(m.Bit(1), 2)) == "UInt[2](1)"


def test_sint_of_bit():
    class Foo(m.Circuit):
        assert repr(m.sint(m.Bit(1), 2)) == "SInt[2](-1)"


def test_array_1_nested():
    class Foo(m.Circuit):
        assert isinstance(m.array([m.bits(0, 3)]), m.Array[1, m.Bits[3]])
