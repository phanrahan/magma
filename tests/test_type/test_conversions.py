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
    zext, sext
    # tuple_, Tuple, \
from magma.bitutils import seq2int
import magma as m

def test_bit():
    assert isinstance(bit(0)._value, Bit)
    assert isinstance(bit(1)._value, Bit)
    assert isinstance(bit(VCC)._value, Bit)
    assert isinstance(bit(GND)._value, Bit)
    assert isinstance(bit(bit(0))._value, Bit)
    assert isinstance(bit(clock(0))._value, Bit)
    assert isinstance(bit(reset(0))._value, Bit)
    assert isinstance(bit(enable(0))._value, Bit)
    assert isinstance(bit(bits(0,1))._value, Bit)
    assert isinstance(bit(uint(0,1))._value, Bit)
    assert isinstance(bit(sint(0,1))._value, Bit)

def test_enable():
    assert isinstance(enable(0)._value, Enable)
    assert isinstance(enable(1)._value, Enable)
    assert isinstance(enable(VCC)._value, Enable)
    assert isinstance(enable(GND)._value, Enable)
    assert isinstance(enable(bit(0))._value, Enable)
    assert isinstance(enable(clock(0))._value, Enable)
    assert isinstance(enable(reset(0))._value, Enable)
    assert isinstance(enable(enable(0))._value, Enable)
    assert isinstance(enable(bits(0,1))._value, Enable)
    assert isinstance(enable(uint(0,1))._value, Enable)
    assert isinstance(enable(sint(0,1))._value, Enable)

def test_reset():
    assert isinstance(reset(0)._value, Reset)
    assert isinstance(reset(1)._value, Reset)
    assert isinstance(reset(VCC)._value, Reset)
    assert isinstance(reset(GND)._value, Reset)
    assert isinstance(reset(bit(0))._value, Reset)
    assert isinstance(reset(clock(0))._value, Reset)
    assert isinstance(reset(enable(0))._value, Reset)
    assert isinstance(reset(reset(0))._value, Reset)
    assert isinstance(reset(bits(0,1))._value, Reset)
    assert isinstance(reset(uint(0,1))._value, Reset)
    assert isinstance(reset(sint(0,1))._value, Reset)

def test_clock():
    assert isinstance(clock(0)._value, Clock)
    assert isinstance(clock(1)._value, Clock)
    assert isinstance(clock(VCC)._value, Clock)
    assert isinstance(clock(GND)._value, Clock)
    assert isinstance(clock(bit(0))._value, Clock)
    assert isinstance(clock(clock(0))._value, Clock)
    assert isinstance(clock(reset(0))._value, Clock)
    assert isinstance(clock(enable(0))._value, Clock)
    assert isinstance(clock(bits(0,1))._value, Clock)
    assert isinstance(clock(uint(0,1))._value, Clock)
    assert isinstance(clock(sint(0,1))._value, Clock)

def test_array():
     assert isinstance(array(1,4)._value, Array)
     assert isinstance(array([1,0,0,0])._value, Array)
     assert isinstance(array(VCC)._value, Array)
     assert isinstance(array(array(1,4))._value, Array)
     assert isinstance(array(uint(1,4))._value, Array)
     assert isinstance(array(sint(1,4))._value, Array)

def test_bits():
     assert isinstance(bits(1,4)._value, Bits)
     assert isinstance(bits([1,0,0,0])._value, Bits)
     assert isinstance(bits(VCC)._value, Bits)
     assert isinstance(bits(array(1,4))._value, Bits)
     assert isinstance(bits(uint(1,4))._value, Bits)
     assert isinstance(bits(sint(1,4))._value, Bits)

def test_uint():
     assert isinstance(uint(1,4)._value, UInt)
     assert isinstance(uint([1,0,0,0])._value, UInt)
     assert isinstance(uint(VCC)._value, UInt)
     assert isinstance(uint(array(1,4))._value, UInt)
     assert isinstance(uint(bits(1,4))._value, UInt)
     #assert isinstance(uint(sint(1,4))._value, UInt)

def test_sint():
     assert isinstance(sint(1,4)._value, SInt)
     assert isinstance(sint([1,0,0,0])._value, SInt)
     assert isinstance(sint(VCC)._value, SInt)
     assert isinstance(sint(array(1,4))._value, SInt)
     assert isinstance(sint(bits(1,4))._value, SInt)
     #assert isinstance(sint(sint(1,4))._value, SInt)

# def test_tuple():
#      assert isinstance(tuple_(OrderedDict(x=0, y=1)), Tuple)
#      assert isinstance(tuple_([0,1]), Tuple)
#      assert isinstance(tuple_(VCC), Tuple)
#      assert isinstance(tuple_(array(1,4)), Tuple)
#      assert isinstance(tuple_(bits(1,4)), Tuple)
#      assert isinstance(tuple_(sint(1,4)), Tuple)
#      assert isinstance(tuple_(uint(1,4)), Tuple)


@pytest.mark.parametrize("type_,value",
                         product([bits, sint, uint], [-5, 0, 10]))
def test_zext(type_, value):
    if type_ != sint:
        value = abs(value)
    in_ = type_(value, 16)
    # TODO(rsetaluri): Ideally, zext(bits) should return an object of type
    # Bits, instead it returns an object of type Array. For now, we wrap
    # the result of zext() in bits().
    out = type_(zext(in_, 16))
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
        a = m.In(m.SInt[2])()
        op(a, 2)
        assert False, "This should raise an exception"
    except Exception as e:
        assert str(e) == f"{op.__name__} only works with non input values"


@pytest.mark.parametrize("op", [m.zext, m.sext])
def test_extension_no_error(op):
    try:
        a = m.Wire(m.SInt[2])
        op(a, 2)
    except Exception as e:
        assert False, "This should work"
