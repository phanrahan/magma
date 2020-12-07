import pytest
import magma as m


def test_adc_signed_unsigned():
    Data = m.Bits[16]
    UData = m.UInt[16]
    SData = m.SInt[16]

    with pytest.raises(TypeError) as e:
        @m.combinational2()
        def adc(s: m.Bit, a: Data, b: Data) -> (Data, m.Bit):
            if s:
                a = SData(a)
                b = SData(b)
            else:
                a = UData(a)
                b = UData(b)
            return a.adc(b, s)

    assert str(e.value) == ("Found incompatible types SInt[16] and UInt[16] in"
                            " mux inference")
