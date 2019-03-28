import pytest
import magma as m
from magma.testing import check_files_equal


def test_verilog_field_uniquify():
    # https://github.com/phanrahan/magma/issues/330
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
