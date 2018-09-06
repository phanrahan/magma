import magma as m
from magma.testing import check_files_equal


def def_foo():
    foo = m.DefineCircuit("Foo", "ifc", m.Tuple(I=m.In(m.Bit), O=m.Out(m.Bit)))
    m.wire(foo.ifc.I, foo.ifc.O)
    m.EndCircuit()
    return foo


def test_multi_direction_tuple():
    foo = def_foo()
    m.compile("build/test_multi_direction_tuple", foo, output="coreir")
    assert check_files_equal(__file__, f"build/test_multi_direction_tuple.json",
                             f"gold/test_multi_direction_tuple.json")

    assert [T.isinput() for T in foo.interface.ports["ifc"].Ts] == \
           [False, True]

    assert [T.isinput() for T in foo.IO.ports["ifc"].Ts] == \
           [True, False]


def test_multi_direction_tuple_instance():
    bar = m.DefineCircuit("bar", "ifc", m.Tuple(I=m.In(m.Bit), O=m.Out(m.Bit)))
    foo_inst = def_foo()()
    m.wire(bar.ifc.I, foo_inst.ifc.I)
    m.wire(bar.ifc.O, foo_inst.ifc.O)
    m.EndCircuit()

    m.compile("build/test_multi_direction_tuple_instance", bar, output="coreir")
    assert check_files_equal(__file__, f"build/test_multi_direction_tuple_instance.json",
                             f"gold/test_multi_direction_tuple_instance.json")


def test_multi_direction_tuple_instance_bulk():
    bar = m.DefineCircuit("bar", "ifc", m.Tuple(I=m.In(m.Bit), O=m.Out(m.Bit)))
    foo_inst = def_foo()()
    m.wire(bar.ifc, foo_inst.ifc)
    m.EndCircuit()

    m.compile("build/test_multi_direction_tuple_instance_bulk", bar, output="coreir")
    # NOTE: Should be the same as previous test, so we use that as a check
    assert check_files_equal(__file__, f"build/test_multi_direction_tuple_instance_bulk.json",
                             f"gold/test_multi_direction_tuple_instance.json")

def test_nesting():
    bar = m.DefineCircuit("bar", "I", m.Tuple(x=m.In(m.Tuple(a=m.Bit, b=m.Bit)),
                                              y=m.Out(m.Tuple(a=m.Bit, b=m.Bit)),
                                              z=m.Tuple(a=m.In(m.Bit), b=m.Out(m.Bit))))
    foo = def_foo()
    foo_inst0 = foo()
    foo_inst1 = foo()
    foo_inst2 = foo()
    m.wire(foo_inst0.ifc.I, bar.I.x.a)
    m.wire(foo_inst0.ifc.O, bar.I.y.a)
    m.wire(foo_inst1.ifc.I, bar.I.x.b)
    m.wire(foo_inst1.ifc.O, bar.I.y.b)
    m.wire(foo_inst2.ifc.I, bar.I.z.a)
    m.wire(foo_inst2.ifc.O, bar.I.z.b)
    m.EndCircuit()
    m.compile("build/test_nesting", bar, output="coreir")
    assert check_files_equal(__file__, f"build/test_nesting.json",
                             f"gold/test_nesting.json")

def test_array_nesting():
    T = m.Array(10, m.Tuple(I=m.In(m.Bit), O=m.Out(m.Bit)))
    Foo = m.DefineCircuit("Foo", "IFC", T)
    for i in range(10):
        m.wire(Foo.IFC[i].I, Foo.IFC[i].O)
    m.EndCircuit()
    m.compile("build/test_array_nesting", Foo, output="coreir")
    assert check_files_equal(__file__, f"build/test_array_nesting.json",
                             f"gold/test_array_nesting.json")

if __name__ == "__main__":
    test_multi_direction_tuple()
