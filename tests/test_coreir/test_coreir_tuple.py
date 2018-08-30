import magma as m
from magma.testing import check_files_equal


def test_multi_direction_tuple():
    foo = m.DefineCircuit("Foo", "ifc", m.Tuple(I=m.In(m.Bit), O=m.Out(m.Bit)))
    m.wire(foo.ifc.I, foo.ifc.O)
    m.EndCircuit()

    m.compile("build/test_multi_direction_tuple", foo, output="coreir")
    assert check_files_equal(__file__, f"build/test_multi_direction_tuple.json",
                             f"gold/test_multi_direction_tuple.json")

    assert [T.isinput() for T in foo.interface.ports["ifc"].Ts] == \
           [False, True]

    assert [T.isinput() for T in foo.IO.ports["ifc"].Ts] == \
           [True, False]

if __name__ == "__main__":
    test_multi_direction_tuple()
