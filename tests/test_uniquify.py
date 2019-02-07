import magma as m


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
