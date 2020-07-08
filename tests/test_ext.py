import random

import pytest

import magma as m

WIDTH = 4
NTESTS = 8

@pytest.mark.parametrize('T', [m.Bits, m.UInt, m.SInt])
def test_zext(T):
    for _ in range(NTESTS):
        val = random.randrange(1 << WIDTH)
        ext = random.randrange(1, 5)
        a =  T[WIDTH](val)
        b = a.zext(ext)
        assert b.bits() == a.concat(T[ext](0)).bits()


@pytest.mark.parametrize('T', [m.SInt])
def test_sext(T):
    for _ in range(NTESTS):
        val = random.randrange(1 << WIDTH)
        ext = random.randrange(1, 5)
        a =  T[WIDTH](val)
        b = a.sext(ext)
        if (val >> (WIDTH - 1)):
            assert b.bits() == a.concat(T[ext](-1)).bits()
        else:
            assert b.bits() == a.concat(T[ext](0)).bits()


@pytest.mark.parametrize('T', [m.Bits, m.UInt, m.SInt])
def test_ext(T):
    for _ in range(NTESTS):
        val = random.randrange(1 << WIDTH)
        ext = random.randrange(1, 5)
        a =  T[WIDTH](val)
        b = a.ext(ext)
        if T is m.SInt:
            assert b.bits() == a.sext(ext).bits()
        else:
            assert b.bits() == a.zext(ext).bits()


@pytest.mark.parametrize('T', [m.Bits, m.UInt, m.SInt])
def test_types(T):
    a = T[WIDTH]()
    ext = random.randrange(1, 5)
    b = a.zext(ext)
    assert isinstance(b, T)
    if T is m.SInt:
        c = a.sext(ext)
        assert isinstance(c, T)
