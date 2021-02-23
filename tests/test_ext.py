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


def test_ext_n():
    value = m.SInt[32]()

    # zext TypeError.
    with pytest.raises(TypeError) as pytest_e:
        m.zext(value, None)
    assert pytest_e.type is TypeError
    assert pytest_e.value.args == ("Expected non-negative integer, got 'None'",)

    # zext ValueError.
    with pytest.raises(TypeError) as pytest_e:
        m.zext(value, -1)
    assert pytest_e.type is TypeError
    assert pytest_e.value.args == ("Expected non-negative integer, got '-1'",)

    # zext identity.
    assert m.zext(value, 0) is value

    # sext TypeError.
    with pytest.raises(TypeError) as pytest_e:
        m.sext(value, None)
    assert pytest_e.type is TypeError
    assert pytest_e.value.args == ("Expected non-negative integer, got 'None'",)

    # sext ValueError.
    with pytest.raises(TypeError) as pytest_e:
        m.sext(value, -1)
    assert pytest_e.type is TypeError
    assert pytest_e.value.args == ("Expected non-negative integer, got '-1'",)

    # sext identity.
    assert m.sext(value, 0) is value
