import magma as m


_SEQ2INT_CASES = (
    ([1, 0, 1, 1], 13),
    ([True, False, 1, 0], 5),
)
_INT2SEQ_CASES = (
    (14, None, [0, 1, 1, 1]),
    (12, 8, [0, 0, 1, 1, 0, 0, 0, 0]),
)
_CLOG2_CASES = (
    (1, 0),
    (7, 3),
    (14, 4),
    (16, 4),
)
_CLOG2SAFE_CASES = (
    (1, 1),
    (7, 3),
    (14, 4),
    (16, 4),
)


def test_seq2int():
    for s, i in _SEQ2INT_CASES:
        assert m.bitutils.seq2int(s) == i


def test_int2seq():
    for i, n, s in _INT2SEQ_CASES:
        assert m.bitutils.int2seq(i, n=n) == s


def test_clog2():
    for i, o in _CLOG2_CASES:
        assert m.bitutils.clog2(i) == o


def test_clog2safe():
    for i, o in _CLOG2SAFE_CASES:
        assert m.bitutils.clog2safe(i) == o
