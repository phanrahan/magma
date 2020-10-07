import magma as m


def test_struct_eq():
    assert m.Array[3, m.In(m.Bit)] == m.Array[3, m.Out(m.Bit)], """\
Direction should not matter when checking structural equality\
"""

    class T1(m.Product):
        x = m.Bit
        y = m.Out(m.Bits[1])

    class T2(m.Product):
        x = m.In(m.Bit)
        y = m.Bits[1]
    assert T1 is not T2, "Different names are not nominally equal"
    assert m.Array[3, T1] == m.Array[3, T2], """\
Products should match structurally, direction does not matter
"""

    class T3(m.Product):
        x = m.In(m.Bit)
    assert m.Array[3, T1] != m.Array[3, T3], """\
Missing field should not match
"""

    class T4(m.Product):
        x = m.In(m.Bit)
        z = m.Bits[1]
    assert m.Array[3, T1] != m.Array[3, T4], """\
Different fields should not match
"""
