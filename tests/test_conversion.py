import pytest
import magma as m
import hwtypes as ht


def test_concat():
    class Foo(m.Circuit):
        b0 = m.bit(1)
        b1 = m.bits(1, 1)
        bits0 = m.concat(b0, b1)
        bits1 = m.concat(m.bits(b0), b1)
        assert type(bits0) == m.Out(m.Bits[2])


def test_concat_bit():
    class Foo(m.Circuit):
        assert int(m.bits(m.concat(ht.Bit(True), True, m.bits(1)))) == 7


def test_ext():
    class Foo(m.Circuit):
        x0 = m.sint(1, 1)
        x1 = m.zext_by(x0, 2)
        x2 = m.zext_to(x0, 3)
        assert repr(x1) == "SInt[3](1)"
        assert repr(x1) == repr(x2)

        x3 = m.sext_by(x0, 2)
        x4 = m.sext_to(x0, 3)
        assert repr(x3) == "SInt[3](-1)"
        assert repr(x3) == repr(x4)


def test_concat_type_error():
    with pytest.raises(TypeError):
        m.concat(object(), object())


@pytest.mark.parametrize('op', [m.uint, m.sint])
def test_convert_extend(op):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[5]))
        value = op(io.I, 32)
        assert len(value) == 32
        if op is m.sint:
            assert isinstance(type(value.name.inst), m.conversions.ConcatN)
            # Check sext logic
            # TODO(leonardt/array2): Here it would be nice if the trace API could traverse concat nodes
            for x in value.name.inst.I1.trace():
                assert x is io.I[4]
