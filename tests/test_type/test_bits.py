"""
Test the `m.Bits` type
"""

import magma as m

ARRAY2 = m.Array[2, m.Bit]
ARRAY4 = m.Array[4, m.Bit]


def test_bits_basic():
    """
    Basic bits tests
    """
    bits_2 = m.Bits[2]
    bits_in_2 = m.In(m.Bits[2])
    bits_out_2 = m.Out(m.Bits[2])
    assert bits_2 == m.Bits[2]
    assert bits_in_2 == m.In(bits_2)
    assert bits_out_2 == m.Out(bits_2)

    assert bits_2 != bits_in_2
    assert bits_2 != bits_out_2
    assert bits_in_2 != bits_out_2

    bits_4 = m.Bits[4]
    assert bits_4 == ARRAY4
    assert bits_2 != bits_4


def test_val():
    """
    Test instances of Bits[4] work correctly
    """
    bits_4_in = m.In(m.Bits[4])
    bits_4_out = m.Out(m.Bits[4])

    assert m.Flip(bits_4_in) == bits_4_out
    assert m.Flip(bits_4_out) == bits_4_in

    a_0 = bits_4_out(name='a0')
    print(a_0)

    a_1 = bits_4_in(name='a1')
    print(a_1)

    a_1.wire(a_0)

    b_0 = a_1[0]
    assert b_0 is a_1[0], "getitem failed"

    a_3 = a_1[0:2]
    assert a_3 == a_1[0:2], "getitem of slice failed"


def test_flip():
    """
    Test flip interface
    """
    bits_2 = m.Bits[2]
    a_in = m.In(bits_2)
    a_out = m.Out(bits_2)

    print(a_in)
    print(a_out)

    assert a_in != ARRAY2
    assert a_out != ARRAY2
    assert a_in != a_out

    in_a_out = m.In(a_out)
    assert in_a_out == a_in
    print(in_a_out)

    a_out_flipped = m.Flip(a_out)
    assert a_out_flipped == a_in

    out_a_in = m.Out(a_in)
    assert out_a_in == a_out

    a_in_flipped = m.Flip(a_in)
    assert a_in_flipped == a_out
    print(a_in_flipped)


def test_construct():
    """
    Test `m.bits` interface
    """
    a_1 = m.bits([1, 1])
    print(type(a_1))
    assert isinstance(a_1, m.BitsType)


def test_const():
    """
    Test constant constructor interface
    """
    data = m.Bits[16]
    zero = data(0)
    assert zero == m.bits(0, 16)


def test_setitem_bfloat():
    """
    Test constant constructor interface
    """
    class TestCircuit(m.Circuit):
        IO = ["I", m.In(m.BFloat[16]), "O", m.Out(m.BFloat[16])]
        @classmethod
        def definition(io):
            a = io.I
            b = a[0:-1].concat(m.bits(0, 1))
            io.O <= b
    print(repr(TestCircuit))
    assert repr(TestCircuit) == """\
TestCircuit = DefineCircuit("TestCircuit", "I", In(BFloat[16]), "O", Out(BFloat[16]))
wire(TestCircuit.I[0], TestCircuit.O[0])
wire(TestCircuit.I[1], TestCircuit.O[1])
wire(TestCircuit.I[2], TestCircuit.O[2])
wire(TestCircuit.I[3], TestCircuit.O[3])
wire(TestCircuit.I[4], TestCircuit.O[4])
wire(TestCircuit.I[5], TestCircuit.O[5])
wire(TestCircuit.I[6], TestCircuit.O[6])
wire(TestCircuit.I[7], TestCircuit.O[7])
wire(TestCircuit.I[8], TestCircuit.O[8])
wire(TestCircuit.I[9], TestCircuit.O[9])
wire(TestCircuit.I[10], TestCircuit.O[10])
wire(TestCircuit.I[11], TestCircuit.O[11])
wire(TestCircuit.I[12], TestCircuit.O[12])
wire(TestCircuit.I[13], TestCircuit.O[13])
wire(TestCircuit.I[14], TestCircuit.O[14])
wire(0, TestCircuit.O[15])
EndCircuit()\
"""  # noqa
