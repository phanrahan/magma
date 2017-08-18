import pytest
from magma import \
    bit, BitType, GND, VCC, \
    ArrayType, \
    bits, BitsType, \
    uint, UIntType, \
    sint, SIntType
from magma.conversions import array

def test_bit():
    assert isinstance(bit(0), BitType)
    assert isinstance(bit(1), BitType)
    assert isinstance(bit(VCC), BitType)
    assert isinstance(bit(GND), BitType)
    assert isinstance(bit(bits(0,1)), BitType)
    assert isinstance(bit(uint(0,1)), BitType)
    assert isinstance(bit(sint(0,1)), BitType)

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
     assert isinstance(uint(sint(1,4)), UIntType)

def test_sint():
     assert isinstance(sint(1,4), SIntType)
     assert isinstance(sint([1,0,0,0]), SIntType)
     assert isinstance(sint(VCC), SIntType)
     assert isinstance(sint(array(1,4)), SIntType)
     assert isinstance(sint(bits(1,4)), SIntType)
     assert isinstance(sint(sint(1,4)), SIntType)

