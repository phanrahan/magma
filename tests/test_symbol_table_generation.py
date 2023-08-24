import pytest

import magma as m
from magma.symbol_table import SYMBOL_TABLE_EMPTY


def _compile(name, ckt, include_master=False):
    res = m.compile(name, ckt, generate_symbols=True)
    symbol_table = res["symbol_table"]
    if not include_master:
        return res["symbol_table"]
    return res["symbol_table"], res["master_symbol_table"]


class SB_DFF(m.Circuit):
    io = m.IO(D=m.In(m.Bit), Q=m.Out(m.Bit), C=m.In(m.Clock))


def test_symbol_table_dff():

    class DFFInit1(m.Circuit):
        io = m.IO(D=m.In(m.Bit), Q=m.Out(m.Bit), C=m.In(m.Clock))
        dff_inst = SB_DFF()
        dff_inst.D @= ~io.D
        io.Q @= ~dff_inst.Q

    symbol_table = _compile("build/DFFInit1", DFFInit1)
    assert symbol_table.get_module_name("DFFInit1") == "DFFInit1"
    assert (symbol_table.get_instance_name("DFFInit1", "SB_DFF_inst0") ==
            (SYMBOL_TABLE_EMPTY, "SB_DFF_inst0"))
    assert symbol_table.get_port_name("DFFInit1", "D") == "D"
    assert symbol_table.get_port_name("DFFInit1", "Q") == "Q"
    assert symbol_table.get_port_name("DFFInit1", "C") == "C"
    instance_type = symbol_table.get_instance_type("DFFInit1", "SB_DFF_inst0")
    assert instance_type == "SB_DFF"


def test_symbol_table_dff_list():

    class DFFList(m.Circuit):
        io = m.IO(D=m.In(m.Bit), Q=m.Out(m.Bit), C=m.In(m.Clock))
        dffs = []
        prev = io.D
        for i in range(10):
            dff = SB_DFF()
            dffs.append(dff)
            dff.D @= prev
            prev = dff.Q
        io.Q @= prev

    symbol_table = _compile("build/DFFList", DFFList)
    for i in range(10):
        name = symbol_table.get_instance_name("DFFList", f"SB_DFF_inst{i}")
        assert name == (SYMBOL_TABLE_EMPTY, f"SB_DFF_inst{i}")
        instance_type = symbol_table.get_instance_type(
            "DFFList", f"SB_DFF_inst{i}")
        assert instance_type == "SB_DFF"


def test_symbol_table_bundle_flattening():

    class MyBundle(m.Product):
        x = m.Bit
        y = m.Bit

    class WithTuple(m.Circuit):
        io = m.IO(
            I1=m.In(MyBundle),
            O=m.Out(MyBundle),
            I2=m.In(m.Bit)
        )
        io.O.undriven()

    symbol_table, master_symbol_table = _compile(
        "build/WithTuple", WithTuple, include_master=True)

    # Check magma -> CoreIR mapping.
    assert symbol_table.get_module_name("WithTuple") == "WithTuple"
    assert symbol_table.get_port_name("WithTuple", "I1") == "I1"
    assert symbol_table.get_port_name("WithTuple", "O") == "O"
    assert symbol_table.get_port_name("WithTuple", "I2") == "I2"
    # Check that "I.x" is not mapped at this level.
    with pytest.raises(Exception):
        symbol_table.get_port_name("WithTuple", "I1.x")

    # Check magma -> Verilog (master) mapping.
    assert master_symbol_table.get_port_name("WithTuple", "I1.x") == "I1_x"
    assert master_symbol_table.get_port_name("WithTuple", "I1.y") == "I1_y"
    assert master_symbol_table.get_port_name("WithTuple", "O.x") == "O_x"
    assert master_symbol_table.get_port_name("WithTuple", "O.y") == "O_y"
    # Check that top-level port "I1" is not mapped in the master mapping.
    with pytest.raises(Exception):
        master_symbol_table.get_port_name("WithTuple", "I1")
    assert master_symbol_table.get_port_name("WithTuple", "I2") == "I2"


def test_symbol_table_inlining_example():

    class X(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

    class Bar(m.Circuit):
        _INLINED_ = True
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        x = X(name="x")
        io.O @= x(io.I)

    class Baz(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        bar = Bar(name="bar")
        io.O @= bar(io.I)

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        bar = Bar(name="bar")
        io.O @= bar(io.I)

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        foo = Foo(name="foo")
        baz = Baz(name="baz")
        io.O @= foo(baz(io.I))

    symbol_table = _compile("build/Top", Top)
    # NOTE: These two conditions would only hold in the post-CoreIR
    # mapping. Since we only test the magma-to-CoreIR symbol table for now,
    # these will not hold.
    #
    # assert (symbol_table.get_instance_name("Foo", "bar") ==
    #         m.symbol_table.INLINED)
    # assert symbol_table.get_inlined_instance_name("Foo", "bar", "x") == "bar_x"


def test_symbol_table_nested_inlining():

    class X(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

    class Bar(m.Circuit):
        _INLINED_ = True
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        x = X(name="x")
        io.O @= x(io.I)

    class Baz(m.Circuit):
        _INLINED_ = True
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        bar = Bar(name="bar")
        io.O @= bar(io.I)

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        bar = Bar(name="bar")
        io.O @= bar(io.I)

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        foo = Foo(name="foo")
        baz = Baz(name="baz")
        io.O @= foo(baz(io.I))

    symbol_table = _compile("build/Top", Top)
    # NOTE: These two conditions would only hold in the post-CoreIR
    # mapping. Since we only test the magma-to-CoreIR symbol table for now,
    # these will not hold.
    #
    # assert symbol_table.get_instance_name("Top", "baz") == m.symbol_table.INLINED
    # assert symbol_table.get_instance_name("Foo", "bar") == m.symbol_table.INLINED
    # assert symbol_table.get_inlined_instance_name("Top", "baz", "bar", "x") == "baz_bar_x"
