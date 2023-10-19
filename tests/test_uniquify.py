import pytest
import magma as m
from magma.testing import check_files_equal


def test_verilog_field_uniquify():
    # https://github.com/phanrahan/magma/issues/330.
    class HalfAdder(m.Circuit):
        name = "HalfAdder"
        io = m.IO(A=m.In(m.Bit), B=m.In(m.Bit), S=m.Out(m.Bit), C=m.Out(m.Bit))
        io.verilog = """\
            assign S = A ^ B;
            assign C = A & B;\
        """


def test_uniquify_equal():
    class foo(m.Circuit):
        name = "foo"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        m.wire(io.I, io.O)

    class bar(m.Circuit):
        name = "foo"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        m.wire(io.I, io.O)

    class top(m.Circuit):
        name = "top"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        curr = io.I
        for circ in (foo, bar):
            inst = circ()
            m.wire(inst.I, curr)
            curr = inst.O
        m.wire(curr, io.O)

    assert hash(repr(foo)) == hash(repr(bar))

    m.compile("build/uniquify_equal", top, output="coreir")
    assert check_files_equal(__file__,
                             "build/uniquify_equal.json",
                             "gold/uniquify_equal.json")


def test_uniquify_unequal():
    class foo(m.Circuit):
        name = "foo"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        m.wire(io.I, io.O)

    class bar(m.Circuit):
        name = "foo"
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[2]))
        m.wire(io.I, io.O)

    class top(m.Circuit):
        name = "top"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        foo_inst = foo()
        m.wire(io.I, foo_inst.I)
        bar_inst = bar()
        m.wire(foo_inst.O, bar_inst.I[0])
        m.wire(foo_inst.O, bar_inst.I[1])
        m.wire(bar_inst.O[0], io.O)

    assert hash(repr(foo)) != hash(repr(bar))

    m.compile("build/uniquify_unequal", top, output="coreir")
    assert check_files_equal(__file__,
                             "build/uniquify_unequal.json",
                             "gold/uniquify_unequal.json")


def test_key_error():
    default_port_mapping = {
        "I": "in",
        "I0": "in0",
        "I1": "in1",
        "O": "out",
        "S": "sel",
    }

    class I(m.Product):
        data = m.Array[2, m.Bits[6]]
        sel = m.Bits[m.bitutils.clog2(2)]

    class _Mux(m.Circuit):
        name = f"coreir_commonlib_mux{2}x{6}"
        io = m.IO(I=m.In(I), O=m.Out(m.Bits[6]))
        coreir_name = "muxn"
        coreir_lib = "commonlib"
        coreir_genargs = {"width": 6, "N": 2}
        renamed_ports = default_port_mapping

    class Mux2x6(m.Circuit):
        name = "Mux2x6"
        io = m.IO(I0=m.In(m.Bits[6]), I1=m.In(
        m.Bits[6]), S=m.In(m.Bit), O=m.Out(m.Bits[6]))

        mux = _Mux()
        m.wire(io.I0, mux.I.data[0])
        m.wire(io.I1, mux.I.data[1])
        m.wire(io.S, mux.I.sel[0])
        m.wire(mux.O, io.O)

    class MuxWrapper_2_6(m.Circuit):
        name = "MuxWrapper_2_6"
        io = m.IO(I=m.Array[2, m.In(
        m.Bits[6])], S=m.In(m.Bits[1]), O=m.Out(m.Bits[6]))
        Mux2x6_inst0 = Mux2x6()
        m.wire(io.I[0], Mux2x6_inst0.I0)
        m.wire(io.I[1], Mux2x6_inst0.I1)
        m.wire(io.S[0], Mux2x6_inst0.S)
        m.wire(Mux2x6_inst0.O, io.O)

    class MuxWrapper_2_6_copy(m.Circuit):
        name = "MuxWrapper_2_6"
        io = m.IO(I=m.Array[2, m.In(
        m.Bits[6])], S=m.In(m.Bits[1]), O=m.Out(m.Bits[6]))
        Mux2x6_inst0 = Mux2x6()
        m.wire(io.I[0], Mux2x6_inst0.I0)
        m.wire(io.I[1], Mux2x6_inst0.I1)
        m.wire(io.S[0], Mux2x6_inst0.S)
        m.wire(Mux2x6_inst0.O, io.O)

    class MuxWithDefaultWrapper_2_6_19_0(m.Circuit):
        name = "MuxWithDefaultWrapper_2_6_19_0"
        io = m.IO(I=m.Array[2, m.In(
        m.Bits[6])], S=m.In(m.Bits[19]), O=m.Out(m.Bits[6]))
        MuxWrapper_2_6_inst0 = MuxWrapper_2_6()
        MuxWrapper_2_6_inst1 = MuxWrapper_2_6_copy()
        m.wire(io.I, MuxWrapper_2_6_inst0.I)
        m.wire(io.I, MuxWrapper_2_6_inst1.I)
        m.wire(io.S[0], MuxWrapper_2_6_inst0.S[0])
        m.wire(io.S[0], MuxWrapper_2_6_inst1.S[0])
        m.wire(MuxWrapper_2_6_inst1.O, io.O)

    top = MuxWithDefaultWrapper_2_6_19_0
    m.compile(f"build/{top.name}", top, output="coreir")
    assert check_files_equal(__file__,
                             f"build/{top.name}.json",
                             "gold/uniquification_key_error_mux.json")


def test_uniquify_verilog():
    [foo0] = m.define_from_verilog("""
module foo(input I, output O);
    assign O = I;
endmodule""")
    [foo1] = m.define_from_verilog("""
module foo(input II, output OO);
    assign OO = II;
endmodule""")
    assert repr(foo0) != repr(foo1)
    class top(m.Circuit):
        name = "top"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        foo0_inst = foo0()
        foo1_inst = foo1()
        m.wire(io.I, foo0_inst.I)
        m.wire(foo0_inst.O, foo1_inst.II)
        m.wire(foo1_inst.OO, io.O)

    with pytest.raises(Exception) as pytest_e:
        m.compile(f"top", top, output="coreir")
        assert False
    assert pytest_e.type is Exception
    assert pytest_e.value.args == \
        ("Can not rename a verilog wrapped file",)


def test_hash_verilog():
    [foo0] = m.define_from_verilog("""
module foo(input I, output O);
    assign O = I;
endmodule""")
    class foo1(m.Circuit):
        name = "foo"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        is_definition = True

    class top(m.Circuit):
        name = "top"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        foo0_inst = foo0()
        foo1_inst = foo1()
        m.wire(io.I, foo0_inst.I)
        m.wire(foo0_inst.O, foo1_inst.I)
        m.wire(foo1_inst.O, io.O)

    assert repr(foo0) == repr(foo1)

    # Run the uniquification pass as a mechanism to check that foo0 and foo1
    # hash to two different things even though they have the same repr.
    pass_ = m.UniquificationPass(top, None)
    pass_.run()
    foo_seen = pass_.seen["foo"]
    assert len(foo_seen) == 2
    for v in foo_seen.values():
        assert len(v) == 1
    expected_ids_ = {id(v[0]) for v in foo_seen.values()}
    ids_ = {id(foo0), id(foo1)}
    assert expected_ids_ == ids_


def test_same_verilog():
    """
    This test checks that if we have multiple verilog-wrapped circuits with the
    same name and same source, the uniquification pass does *not* try to perform
    a rename. As it does not need to.
    """
    def _generate_foo():
        return m.define_from_verilog("""
module foo(input i, output o);
    assign o = i;
endmodule""")[0]

    class _Cell0(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        foo = _generate_foo()()
        foo.i <= io.I
        io.O <= foo.o

    class _Cell1(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        foo = _generate_foo()()
        foo.i <= io.I
        io.O <= foo.o

    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[2]))

        cell0 = _Cell0()
        cell1 = _Cell1()
        cell0.I <= io.I[0]
        cell1.I <= io.I[1]
        io.O[0] <= cell0.O
        io.O[1] <= cell1.O

    # Check that uniq. pass runs successfully.
    pass_ = m.UniquificationPass(_Top, None)
    pass_.run()


def test_multiple_renamed():
    def _gen_foo(width):
        class Foo(m.Circuit):
            io = m.IO(I=m.In(m.Bits[width]), O=m.Out(m.Bits[width]))

            io. O <= io.I

        return Foo

    Foo0 = _gen_foo(2)
    Foo1 = _gen_foo(3)
    Foo2 = _gen_foo(3)

    class _Top(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bits[2]),
            I1=m.In(m.Bits[3]),
            I2=m.In(m.Bits[3]),
            O0=m.Out(m.Bits[2]),
            O1=m.Out(m.Bits[3]),
            O2=m.Out(m.Bits[3]),
        )

        foo0 = Foo0()
        foo1 = Foo1()
        foo2 = Foo2()

        foo0.I <= io.I0
        io.O0 <= foo0.O

        foo1.I <= io.I1
        io.O1 <= foo1.O

        foo2.I <= io.I2
        io.O2 <= foo2.O

    BASENAME = "uniquify_multiple_rename"
    m.compile(f"build/{BASENAME}", _Top, output="coreir")
    assert check_files_equal(__file__,
                             f"build/{BASENAME}.json",
                             f"gold/{BASENAME}.json")


def test_reset_names():

    def _make_foo(width: int):

        class _Foo(m.Circuit):
            name = "Foo"
            io = m.IO(I=m.In(m.Bits[width]), O=m.Out(m.Bits[width]))
            io.O @= io.I

        return _Foo

    Foo1 = _make_foo(1)
    Foo2 = _make_foo(2)

    class _Top1(m.Circuit):
        name = "Top1"
        io = m.IO(I=m.In(m.Bits[3]), O=m.Out(m.Bits[3]))
        io.O[0:1] @= Foo1()(io.I[0:1])
        io.O[1:3] @= Foo2()(io.I[1:3])

    # Because _Top1 has instances of 2 different circuits with the name "Foo",
    # we expect one of them to be uniquified to "Foo_unq1".
    basename = "uniquify_reset_names_1"
    m.compile(f"build/{basename}", _Top1, output="coreir")
    assert check_files_equal(
        __file__, f"build/{basename}.json", f"gold/{basename}.json")

    # Names of circuits should be reset after compilation, even though they were
    # uniquified temporarily.
    assert Foo1.name == "Foo"
    assert Foo2.name == "Foo"

    # We make sure to clear the CoreIR context.
    m.frontend.coreir_.ResetCoreIR()
    m.generator.reset_generator_cache()

    Foo3 = _make_foo(3)

    # Define a new top circuit which will contain instances of *3* different
    # circuits each with the name "Foo". If names were not reset after
    # uniquification above, then there will be a conflict. In particular, Foo3
    # will be renamed to "Foo_unq1" even though Foo2 is already named "Foo_unq1"
    # (*if* names were *not* reset).
    class _Top2(m.Circuit):
        name = "Top2"
        io = m.IO(I=m.In(m.Bits[6]), O=m.Out(m.Bits[6]))
        io.O[0:1] @= Foo1()(io.I[0:1])
        io.O[1:3] @= Foo2()(io.I[1:3])
        io.O[3:6] @= Foo3()(io.I[3:6])

    basename = "uniquify_reset_names_2"
    m.compile(f"build/{basename}", _Top2, output="coreir")
    assert check_files_equal(
        __file__, f"build/{basename}.json", f"gold/{basename}.json")
