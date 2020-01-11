import magma as m


class t(m.Product):
    a = m.Bit
    b = m.Bit
    c = m.Bit


def test_pretty_print_tuple():
    assert m.util.pretty_str(t) == """\
Tuple(
    a = Bit,
    b = Bit,
    c = Bit
)\
"""


def test_pretty_print_tuple_recursive():

    class u(m.Product):
        x = t
        y = t
    assert m.util.pretty_str(u) == """\
Tuple(
    x = Tuple(
        a = Bit,
        b = Bit,
        c = Bit
    ),
    y = Tuple(
        a = Bit,
        b = Bit,
        c = Bit
    )
)\
"""


def test_pretty_print_array_of_tuple():
    u = m.Array[3, t]
    assert m.util.pretty_str(u) == """\
Array[3, Tuple(
    a = Bit,
    b = Bit,
    c = Bit
)]\
"""


def test_pretty_print_array_of_nested_tuple():
    class t(m.Product):
        a = m.Bits[5]
        b = m.UInt[3]
        c = m.SInt[4]

    class u(m.Product):
        x = t
        y = t
    v = m.Array[3, u]
    assert m.util.pretty_str(v) == """\
Array[3, Tuple(
    x = Tuple(
        a = Bits[5],
        b = UInt[3],
        c = SInt[4]
    ),
    y = Tuple(
        a = Bits[5],
        b = UInt[3],
        c = SInt[4]
    )
)]\
"""
