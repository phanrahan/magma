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
        name = f"Mux{height}" + (f"_x{width}" if width else "")
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
    @m.circuit.combinational
    def TestIfStatementBasics(I: m.Bits(2), S: m.Bit) -> m.Bit:
        if S:
            return I[0]
        else:
            return I[1]
    m.compile("build/test_if_statement_basic", TestIfStatementBasics)
    assert check_files_equal(__file__, f"build/test_if_statement_basic.v",
                             f"gold/test_if_statement_basic.v")


def test_if_statement_nested():
    @m.circuit.combinational
    def TestIfStatementNested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
        if S[0]:
            if S[1]:
                return I[0]
            else:
                return I[1]
        else:
            if S[1]:
                return I[2]
            else:
                return I[3]
    m.compile("build/test_if_statement_nested", TestIfStatementNested)
    assert check_files_equal(__file__, f"build/test_if_statement_nested.v",
                             f"gold/test_if_statement_nested.v")


def test_ternary():
    @m.circuit.combinational
    def TestTernary(I: m.Bits(2), S: m.Bit) -> m.Bit:
        return I[0] if S else I[1]
    m.compile("build/test_ternary", TestTernary)
    assert check_files_equal(__file__, f"build/test_ternary.v",
                             f"gold/test_ternary.v")


def test_ternary_nested():
    @m.circuit.combinational
    def TestTernaryNested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
        return I[0] if S[0] else I[1] if S[1] else I[2]
    m.compile("build/test_ternary_nested", TestTernaryNested)
    assert check_files_equal(__file__, f"build/test_ternary_nested.v",
                             f"gold/test_ternary_nested.v")


def test_ternary_nested2():
    @m.circuit.combinational
    def TestTernaryNested2(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
        return (I[0] if S[0] else I[1]) if S[1] else I[2]
    m.compile("build/test_ternary_nested2", TestTernaryNested2)
    assert check_files_equal(__file__, f"build/test_ternary_nested2.v",
                             f"gold/test_ternary_nested2.v")
