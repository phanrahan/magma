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

    assert hash(foo) == hash(bar)

    m.compile("build/uniquify_equal", top, output="coreir")
    assert check_files_equal(__file__,
                             "build/uniquify_equal.json",
                             "gold/uniquify_equal.json")


def test_uniquify_unequal():
    foo = m.DefineCircuit("foo", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    m.wire(foo.I, foo.O)
    m.EndCircuit()

    bar = m.DefineCircuit("foo", "I", m.In(m.Bits(2)), "O", m.Out(m.Bits(2)))
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

    assert hash(foo) != hash(bar)

    m.compile("build/uniquify_unequal", top, output="coreir")
    assert check_files_equal(__file__,
                             "build/uniquify_unequal.json",
                             "gold/uniquify_unequal.json")
