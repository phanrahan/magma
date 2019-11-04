import magma as m
from magma.testing import check_files_equal


class T(m.Product, cache=True):
    I = m.In(m.Bit)
    O = m.Out(m.Bit)

def def_foo():
    foo = m.DefineCircuit("Foo", "ifc", T)
    m.wire(foo.ifc.I, foo.ifc.O)
    m.EndCircuit()
    return foo


def test_multi_direction_tuple():
    foo = def_foo()
    m.compile("build/test_multi_direction_tuple", foo, output="coreir")
    assert check_files_equal(__file__, f"build/test_multi_direction_tuple.json",
                             f"gold/test_multi_direction_tuple.json")

    assert [T.is_input() for T in foo.interface.ports["ifc"]._get_values()] == \
           [False, True]

    assert [T.is_input() for T in foo.IO.ports["ifc"].field_dict.values()] == \
           [True, False]


def test_multi_direction_tuple_instance():
    bar = m.DefineCircuit("bar", "ifc", T)
    foo_inst = def_foo()()
    m.wire(bar.ifc.I, foo_inst.ifc.I)
    m.wire(bar.ifc.O, foo_inst.ifc.O)
    m.EndCircuit()

    m.compile("build/test_multi_direction_tuple_instance", bar, output="coreir")
    assert check_files_equal(__file__, f"build/test_multi_direction_tuple_instance.json",
                             f"gold/test_multi_direction_tuple_instance.json")


def test_multi_direction_tuple_instance_bulk():
    bar = m.DefineCircuit("bar", "ifc", T)
    foo_inst = def_foo()()
    m.wire(bar.ifc, foo_inst.ifc)
    m.EndCircuit()

    m.compile("build/test_multi_direction_tuple_instance_bulk", bar, output="coreir")
    # NOTE: Should be the same as previous test, so we use that as a check
    assert check_files_equal(__file__, f"build/test_multi_direction_tuple_instance_bulk.json",
                             f"gold/test_multi_direction_tuple_instance.json")


class AB(m.Product, cache=True):
    a = m.Bit
    b = m.Bit


class Z(m.Product, cache=True):
    a = m.In(m.Bit)
    b = m.Out(m.Bit)


class Bar(m.Product, cache=True):
    x = m.In(AB)
    y = m.Out(AB)
    z = Z

def test_nesting():
    bar = m.DefineCircuit("bar", "I", Bar)
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


class IO(m.Product, cache=True):
    I = m.In(m.Bit)
    O = m.Out(m.Bit)


def test_array_nesting():
    T = m.Array[10, IO]
    Foo = m.DefineCircuit("Foo", "IFC", T)
    for i in range(10):
        m.wire(Foo.IFC[i].I, Foo.IFC[i].O)
    m.EndCircuit()
    m.compile("build/test_array_nesting", Foo, output="coreir")
    assert check_files_equal(__file__, f"build/test_array_nesting.json",
                             f"gold/test_array_nesting.json")


def test_anon_tuple():
    foo = m.DefineCircuit("Foo", "ifc", m.Tuple[m.In(m.Bit), m.Out(m.Bit)])
    m.wire(foo.ifc[0], foo.ifc[1])
    m.EndCircuit()
    m.compile("build/test_anon_tuple", foo, output="coreir")
    assert check_files_equal(__file__, f"build/test_anon_tuple.json",
                             f"gold/test_anon_tuple.json")


def test_nested_anon_tuple():
    foo = m.DefineCircuit("Foo", "ifc", m.Array[2, m.Tuple[m.In(m.Bit), m.Out(m.Bit)]])
    m.wire(foo.ifc[0][0], foo.ifc[1][1])
    m.wire(foo.ifc[1][0], foo.ifc[0][1])
    m.EndCircuit()
    m.compile("build/test_nested_anon_tuple", foo, output="coreir")
    assert check_files_equal(__file__, f"build/test_nested_anon_tuple.json",
                             f"gold/test_nested_anon_tuple.json")


def test_anon_tuple_nested_array():
    foo = m.DefineCircuit("Foo", "ifc", m.Tuple[m.In(m.Bits[2]), m.Out(m.Bits[2])])
    m.wire(foo.ifc[0][0], foo.ifc[1][1])
    m.wire(foo.ifc[0][1], foo.ifc[1][0])
    m.EndCircuit()
    m.compile("build/test_anon_tuple_nested_array", foo, output="coreir")
    assert check_files_equal(__file__, f"build/test_anon_tuple_nested_array.json",
                             f"gold/test_anon_tuple_nested_array.json")

if __name__ == "__main__":
    test_multi_direction_tuple()
