import pytest
import magma as m
from magma.testing import check_files_equal


def test_verilog_field_uniquify():
    # https://github.com/phanrahan/magma/issues/330.
    HalfAdder = m.DefineCircuit('HalfAdder', 'A', m.In(m.Bit), 'B',
                                m.In(m.Bit), 'S', m.Out(m.Bit), 'C',
                                m.Out(m.Bit))
    HalfAdder.verilog = '''\
        assign S = A ^ B;
        assign C = A & B;\
    '''
    m.EndCircuit()


def test_uniquify_equal():
    foo = m.DefineCircuit("foo", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    m.wire(foo.I, foo.O)
    m.EndCircuit()

    bar = m.DefineCircuit("foo", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    m.wire(bar.I, bar.O)
    m.EndCircuit()

    top = m.DefineCircuit("top", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    curr = top.I
    for circ in (foo, bar):
        inst = circ()
        m.wire(inst.I, curr)
        curr = inst.O
    m.wire(curr, top.O)
    m.EndCircuit()

    assert hash(repr(foo)) == hash(repr(bar))

    m.compile("build/uniquify_equal", top, output="coreir")
    assert check_files_equal(__file__,
                             "build/uniquify_equal.json",
                             "gold/uniquify_equal.json")


def test_uniquify_unequal():
    foo = m.DefineCircuit("foo", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    m.wire(foo.I, foo.O)
    m.EndCircuit()

    bar = m.DefineCircuit("foo", "I", m.In(m.Bits[2]), "O", m.Out(m.Bits[2]))
    m.wire(bar.I, bar.O)
    m.EndCircuit()

    top = m.DefineCircuit("top", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    foo_inst = foo()
    m.wire(top.I, foo_inst.I)
    bar_inst = bar()
    m.wire(foo_inst.O, bar_inst.I[0])
    m.wire(foo_inst.O, bar_inst.I[1])
    m.wire(bar_inst.O[0], top.O)
    m.EndCircuit()

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

    def DeclareCoreirCircuit(*args, **kwargs):
        return m.DeclareCircuit(*args, **kwargs,
                                renamed_ports=default_port_mapping)

    Mux2x6 = m.DefineCircuit("Mux2x6", "I0", m.In(m.Bits[6]), "I1", m.In(m.Bits[6]), "S", m.In(m.Bit), "O", m.Out(m.Bits[6]))
    mux = DeclareCoreirCircuit(f"coreir_commonlib_mux{2}x{6}",
                               *["I", m.In(m.Tuple(data=m.Array[2, m.Bits[6]],
                                                   sel=m.Bits[m.bitutils.clog2(2)])),
                                 "O", m.Out(m.Bits[6])],
                               coreir_name="muxn",
                               coreir_lib="commonlib",
                               coreir_genargs={"width": 6, "N": 2})()
    m.wire(Mux2x6.I0, mux.I.data[0])
    m.wire(Mux2x6.I1, mux.I.data[1])
    m.wire(Mux2x6.S, mux.I.sel[0])
    m.wire(mux.O, Mux2x6.O)
    m.EndDefine()

    MuxWrapper_2_6 = m.DefineCircuit("MuxWrapper_2_6", "I", m.Array[2,m.In(m.Bits[6])], "S", m.In(m.Bits[1]), "O", m.Out(m.Bits[6]))
    Mux2x6_inst0 = Mux2x6()
    m.wire(MuxWrapper_2_6.I[0], Mux2x6_inst0.I0)
    m.wire(MuxWrapper_2_6.I[1], Mux2x6_inst0.I1)
    m.wire(MuxWrapper_2_6.S[0], Mux2x6_inst0.S)
    m.wire(Mux2x6_inst0.O, MuxWrapper_2_6.O)
    m.EndCircuit()

    MuxWrapper_2_6_copy = m.DefineCircuit("MuxWrapper_2_6", "I", m.Array[2,m.In(m.Bits[6])], "S", m.In(m.Bits[1]), "O", m.Out(m.Bits[6]))
    Mux2x6_inst0 = Mux2x6()
    m.wire(MuxWrapper_2_6_copy.I[0], Mux2x6_inst0.I0)
    m.wire(MuxWrapper_2_6_copy.I[1], Mux2x6_inst0.I1)
    m.wire(MuxWrapper_2_6_copy.S[0], Mux2x6_inst0.S)
    m.wire(Mux2x6_inst0.O, MuxWrapper_2_6_copy.O)
    m.EndCircuit()

    MuxWithDefaultWrapper_2_6_19_0 = m.DefineCircuit("MuxWithDefaultWrapper_2_6_19_0", "I", m.Array[2,m.In(m.Bits[6])], "S", m.In(m.Bits[19]), "O", m.Out(m.Bits[6]))
    MuxWrapper_2_6_inst0 = MuxWrapper_2_6()
    MuxWrapper_2_6_inst1 = MuxWrapper_2_6_copy()
    m.wire(MuxWithDefaultWrapper_2_6_19_0.I, MuxWrapper_2_6_inst0.I)
    m.wire(MuxWithDefaultWrapper_2_6_19_0.I, MuxWrapper_2_6_inst1.I)
    m.wire(MuxWithDefaultWrapper_2_6_19_0.S[0], MuxWrapper_2_6_inst0.S[0])
    m.wire(MuxWithDefaultWrapper_2_6_19_0.S[0], MuxWrapper_2_6_inst1.S[0])
    m.wire(MuxWrapper_2_6_inst1.O, MuxWithDefaultWrapper_2_6_19_0.O)
    m.EndCircuit()

    top = MuxWithDefaultWrapper_2_6_19_0
    m.compile(f"build/{top.name}", top, output="coreir")
    assert check_files_equal(__file__,
                             f"build/{top.name}.json",
                             "gold/uniquification_key_error_mux.json")


def test_uniquify_verilog():
    [foo0] = m.DefineFromVerilog("""
module foo(input I, output O);
    assign O = I;
endmodule""")
    [foo1] = m.DefineFromVerilog("""
module foo(input II, output OO);
    assign OO = II;
endmodule""")
    assert repr(foo0) != repr(foo1)
    top = m.DefineCircuit("top", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    foo0_inst = foo0()
    foo1_inst = foo1()
    m.wire(top.I, foo0_inst.I)
    m.wire(foo0_inst.O, foo1_inst.II)
    m.wire(foo1_inst.OO, top.O)
    m.EndDefine()

    with pytest.raises(Exception) as pytest_e:
        m.compile(f"top", top, output="coreir")
        assert False
    assert pytest_e.type is Exception
    assert pytest_e.value.args == \
        ("Can not rename a verilog wrapped file",)


def test_hash_verilog():
    [foo0] = m.DefineFromVerilog("""
module foo(input I, output O);
    assign O = I;
endmodule""")
    foo1 = m.DefineCircuit("foo", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    m.EndCircuit()

    top = m.DefineCircuit("top", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    foo0_inst = foo0()
    foo1_inst = foo1()
    m.wire(top.I, foo0_inst.I)
    m.wire(foo0_inst.O, foo1_inst.I)
    m.wire(foo1_inst.O, top.O)
    m.EndDefine()

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
        return m.DefineFromVerilog("""
module foo(input i, output o);
    assign o = i;
endmodule""")[0]


    class _Cell0(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            foo = _generate_foo()()
            foo.i <= io.I
            io.O <= foo.o


    class _Cell1(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            foo = _generate_foo()()
            foo.i <= io.I
            io.O <= foo.o


    class _Top(m.Circuit):
        IO = ["I", m.In(m.Bits[2]), "O", m.Out(m.Bits[2])]

        @classmethod
        def definition(io):
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
            IO = ["I", m.In(m.Bits[width]), "O", m.Out(m.Bits[width])]

            @classmethod
            def definition(io):
                io. O <= io.I

        return Foo

    Foo0 = _gen_foo(2)
    Foo1 = _gen_foo(3)
    Foo2 = _gen_foo(3)

    class _Top(m.Circuit):
        IO = [
            "I0", m.In(m.Bits[2]),
            "I1", m.In(m.Bits[3]),
            "I2", m.In(m.Bits[3]),
            "O0", m.Out(m.Bits[2]),
            "O1", m.Out(m.Bits[3]),
            "O2", m.Out(m.Bits[3]),
        ]

        @classmethod
        def definition(io):
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
