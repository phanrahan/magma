import magma as m


def test_cache():
    class Main0(m.Circuit):
        name = "Main"
        IO = ["I", m.In(m.Bits(2)), "O", m.Out(m.Bits(2))]
        @classmethod
        def definition(io):
            m.wire(io.I, io.O)

    class Main1(m.Circuit):
        name = "Main"
        IO = ["I", m.In(m.UInt(2)), "O", m.Out(m.UInt(2))]
        @classmethod
        def definition(io):
            m.wire(io.I, io.O)

    assert Main0 is Main1, "Main1 should be the cached version of Main0 since it has the same name"


def test_no_cache():
    class Main0(m.Circuit):
        name = "Main"
        IO = ["I", m.In(m.Bits(2)), "O", m.Out(m.Bits(2))]
        @classmethod
        def definition(io):
            m.wire(io.I, io.O)

    class Main1(m.Circuit):
        __magma_no_cache__ = True
        name = "Main"
        IO = ["I", m.In(m.UInt(2)), "O", m.Out(m.UInt(2))]
        @classmethod
        def definition(io):
            m.wire(io.I, io.O)

    assert Main0 is not Main1, "__magma_no_cache__ is set so they should not be the same"

    Main2 = m.DefineCircuit("Main", "I", m.In(m.SInt(2)), "O",
                            m.Out(m.SInt(2)), __magma_no_cache__=True)
    m.EndDefine()

    assert Main0 is not Main2, "__magma_no_cache__ is set so they should not be the same"
