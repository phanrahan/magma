import magma as m
from magma.testing import check_files_equal


@m.cache_definition
def DefineMux(height=2, width=None):
    if width is None:
        T = m.Bit
    else:
        T = m.Bits(width)

    io = []
    for i in range(height):
        io += ["I{}".format(i), m.In(T)]
    if height == 2:
        select_type = m.Bit
    else:
        select_type = m.Bits(m.bitutils.clog2(height))
    io += ['S', m.In(select_type)]
    io += ['O', m.Out(T)]

    class _Mux(m.Circuit):
        name = "Mux{}x{}".format(height, width)
        IO = io
    return _Mux


def Mux(height=2, width=None, **kwargs):
    return DefineMux(height, width)(**kwargs)


def get_length(value):
    if isinstance(value, m._BitType):
        return None
    elif isinstance(value, m.ArrayType):
        return len(value)
    else:
        raise NotImplementedError(f"Cannot get_length of {type(value)}")


def mux(I, S):
    if isinstance(S, int):
        return I[S]
    elif S.const():
        return I[m.bitutils.seq2int(S.bits())]
    return Mux(len(I), get_length(I[0]))(*I, S)


def test_if_statement_basic():
    class TestIfStatementBasic(m.Circuit):
        IO = ["I", m.In(m.Bits(2)), "S", m.In(m.Bit), "O", m.Out(m.Bit)]

        @m.circuit_def
        def definition(io):
            if io.S:
                O = io.I[0]
                # m.wire(io.O, io.I[0])
                # io.O = io.I[0]
                # TODO: Alternative syntax
                # io.O <= io.I[0]
                # TODO: Or we could use wire syntax
                # wire(io.O, io.I[0])
            else:
                O = io.I[1]
            m.wire(O, io.O)
    m.compile("build/test_if_statement_basic", TestIfStatementBasic)
    assert check_files_equal(__file__, f"build/test_if_statement_basic.v",
                             f"gold/test_if_statement_basic.v")


def test_ternary():
    class TestTernary(m.Circuit):
        IO = ["I", m.In(m.Bits(2)), "S", m.In(m.Bit), "O", m.Out(m.Bit)]

        @m.circuit_def
        def definition(io):
            m.wire(io.O, io.I[0] if io.S else io.I[1])
            # io.O = io.I[0] if io.S else io.I[1]
            # TODO: Or non block assign?
            # io.O <= io.I[0] if io.S else io.[1]
    m.compile("build/test_ternary", TestTernary)
    assert check_files_equal(__file__, f"build/test_ternary.v",
                             f"gold/test_ternary.v")
