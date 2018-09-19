import pytest
from itertools import product
from collections import OrderedDict
from magma import \
    GND, VCC, \
    bit, BitType, \
    clock, ClockType, \
    reset, ResetType, \
    enable, EnableType, \
    array, ArrayType, \
    bits, BitsType, \
    uint, UIntType, \
    sint, SIntType, \
    tuple_, TupleType, \
    zext, sext
from magma.bitutils import seq2int

def test_bit():
    assert isinstance(bit(0), BitType)
    assert isinstance(bit(1), BitType)
    assert isinstance(bit(VCC), BitType)
    assert isinstance(bit(GND), BitType)
    assert isinstance(bit(bit(0)), BitType)
    assert isinstance(bit(clock(0)), BitType)
    assert isinstance(bit(reset(0)), BitType)
    assert isinstance(bit(enable(0)), BitType)
    assert isinstance(bit(bits(0,1)), BitType)
    assert isinstance(bit(uint(0,1)), BitType)
    assert isinstance(bit(sint(0,1)), BitType)

def test_enable():
    assert isinstance(enable(0), EnableType)
    assert isinstance(enable(1), EnableType)
    assert isinstance(enable(VCC), EnableType)
    assert isinstance(enable(GND), EnableType)
    assert isinstance(enable(bit(0)), EnableType)
    assert isinstance(enable(clock(0)), EnableType)
    assert isinstance(enable(reset(0)), EnableType)
    assert isinstance(enable(enable(0)), EnableType)
    assert isinstance(enable(bits(0,1)), EnableType)
    assert isinstance(enable(uint(0,1)), EnableType)
    assert isinstance(enable(sint(0,1)), EnableType)

def test_reset():
    assert isinstance(reset(0), ResetType)
    assert isinstance(reset(1), ResetType)
    assert isinstance(reset(VCC), ResetType)
    assert isinstance(reset(GND), ResetType)
    assert isinstance(reset(bit(0)), ResetType)
    assert isinstance(reset(clock(0)), ResetType)
    assert isinstance(reset(enable(0)), ResetType)
    assert isinstance(reset(reset(0)), ResetType)
    assert isinstance(reset(bits(0,1)), ResetType)
    assert isinstance(reset(uint(0,1)), ResetType)
    assert isinstance(reset(sint(0,1)), ResetType)

def test_clock():
    assert isinstance(clock(0), ClockType)
    assert isinstance(clock(1), ClockType)
    assert isinstance(clock(VCC), ClockType)
    assert isinstance(clock(GND), ClockType)
    assert isinstance(clock(bit(0)), ClockType)
    assert isinstance(clock(clock(0)), ClockType)
    assert isinstance(clock(reset(0)), ClockType)
    assert isinstance(clock(enable(0)), ClockType)
    assert isinstance(clock(bits(0,1)), ClockType)
    assert isinstance(clock(uint(0,1)), ClockType)
    assert isinstance(clock(sint(0,1)), ClockType)

def test_array():
     assert isinstance(array(1,4), ArrayType)
     assert isinstance(array([1,0,0,0]), ArrayType)
     assert isinstance(array(VCC), ArrayType)
     assert isinstance(array(array(1,4)), ArrayType)
     assert isinstance(array(uint(1,4)), ArrayType)
     assert isinstance(array(sint(1,4)), ArrayType)

def test_bits():
     assert isinstance(bits(1,4), BitsType)
     assert isinstance(bits([1,0,0,0]), BitsType)
     assert isinstance(bits(VCC), BitsType)
     assert isinstance(bits(array(1,4)), BitsType)
     assert isinstance(bits(uint(1,4)), BitsType)
     assert isinstance(bits(sint(1,4)), BitsType)

def test_uint():
     assert isinstance(uint(1,4), UIntType)
     assert isinstance(uint([1,0,0,0]), UIntType)
     assert isinstance(uint(VCC), UIntType)
     assert isinstance(uint(array(1,4)), UIntType)
     assert isinstance(uint(bits(1,4)), UIntType)
     #assert isinstance(uint(sint(1,4)), UIntType)

def test_sint():
     assert isinstance(sint(1,4), SIntType)
     assert isinstance(sint([1,0,0,0]), SIntType)
     assert isinstance(sint(VCC), SIntType)
     assert isinstance(sint(array(1,4)), SIntType)
     assert isinstance(sint(bits(1,4)), SIntType)
     #assert isinstance(sint(sint(1,4)), SIntType)

def test_tuple():
     assert isinstance(tuple_(OrderedDict(x=0, y=1)), TupleType)
     assert isinstance(tuple_([0,1]), TupleType)
     assert isinstance(tuple_(VCC), TupleType)
     assert isinstance(tuple_(array(1,4)), TupleType)
     assert isinstance(tuple_(bits(1,4)), TupleType)
     assert isinstance(tuple_(sint(1,4)), TupleType)
     assert isinstance(tuple_(uint(1,4)), TupleType)


@pytest.mark.parametrize("type_,value",
                         product([bits, sint, uint], [-5, 0, 10]))
def test_zext(type_, value):
    if type_ != sint:
        value = abs(value)
    in_ = type_(value, 16)
    # TODO(rsetaluri): Ideally, zext(bits) should return an object of type
    # BitsType, instead it returns an object of type ArrayType. For now, we wrap
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
    # SintType, instead it returns an object of type ArrayType. For now, we wrap
    # the result of zext() in sint().
    out = sint(sext(in_, 16))
    assert len(out.bits()) == 32
    assert int(out) == value
