import random

import pytest

import magma as m

WIDTH = 4
NTESTS = 8


def _check_equal(a, b):
    assert isinstance(type(a.name.inst), m.conversions.ConcatN)
    assert isinstance(type(b.name.inst), m.conversions.ConcatN)
    assert type(a.name.inst.I1.value()) == type(b.name.inst.I1.value())
    assert int(a.name.inst.I1.value()) == int(b.name.inst.I1.value())
    assert a.name.inst.I0.value() is b.name.inst.I0.value()


@pytest.mark.parametrize('T', [m.Bits, m.UInt, m.SInt])
def test_zext(T):
    for _ in range(NTESTS):
        val = random.randrange(1 << WIDTH)
        ext = random.randrange(1, 5)
        a = T[WIDTH](val)
        b = a.zext(ext)
        a = a.concat(T[ext](0))
        _check_equal(a, b)


@pytest.mark.parametrize('T', [m.SInt])
def test_sext(T):
    for _ in range(NTESTS):
        val = random.randrange(1 << WIDTH)
        ext = random.randrange(1, 5)
        a = T[WIDTH](val)
        b = a.sext(ext)
        if (val >> (WIDTH - 1)):
            _check_equal(a.concat(T[ext](-1)), b)
        else:
            _check_equal(a.concat(T[ext](0)), b)


@pytest.mark.parametrize('T', [m.Bits, m.UInt, m.SInt])
def test_ext(T):
    for _ in range(NTESTS):
        val = random.randrange(1 << WIDTH)
        ext = random.randrange(1, 5)
        a = T[WIDTH](val)
        b = a.ext(ext)
        if T is m.SInt:
            _check_equal(a.sext(ext), b)
        else:
            _check_equal(a.zext(ext), b)


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
