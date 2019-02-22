import magma as m
from magma.ssa import ssa
import inspect


def test_basic():
    @ssa
    def basic_if(I: m.Bits(2), S: m.Bit) -> m.Bit:
        if S:
            x = I[0]
        else:
            x = I[1]
        return x

    assert inspect.getsource(basic_if) == """\
def basic_if(I: m.Bits(2), S: m.Bit) ->m.Bit:
    x_0 = I[0]
    x_1 = I[1]
    x_2 = phi([x_1, x_0], S)
    __magma_ssa_return_value_0 = x_2
    O = __magma_ssa_return_value_0
    return O
"""


def test_wat():
    @ssa
    def basic_if(I: m.Bit, S: m.Bit) -> m.Bit:
        x = I
        if S:
            x = x
        else:
            x = x
        return x

    assert inspect.getsource(basic_if) == """\
def basic_if(I: m.Bit, S: m.Bit) ->m.Bit:
    x_0 = I
    x_1 = x_0
    x_2 = x_0
    x_3 = phi([x_2, x_1], S)
    __magma_ssa_return_value_0 = x_3
    O = __magma_ssa_return_value_0
    return O
"""


def test_default():
    @ssa
    def default(I: m.Bits(2), S: m.Bit) -> m.Bit:
        x = I[1]
        if S:
            x = I[0]
        return x

    assert inspect.getsource(default) == """\
def default(I: m.Bits(2), S: m.Bit) ->m.Bit:
    x_0 = I[1]
    x_1 = I[0]
    x_2 = phi([x_0, x_1], S)
    __magma_ssa_return_value_0 = x_2
    O = __magma_ssa_return_value_0
    return O
"""


def test_nested():
    @ssa
    def nested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
        if S[0]:
            if S[1]:
                x = I[0]
            else:
                x = I[1]
        else:
            if S[1]:
                x = I[2]
            else:
                x = I[3]
        return x

    assert inspect.getsource(nested) == """\
def nested(I: m.Bits(4), S: m.Bits(2)) ->m.Bit:
    x_0 = I[0]
    x_1 = I[1]
    x_2 = phi([x_1, x_0], S[1])
    x_3 = I[2]
    x_4 = I[3]
    x_5 = phi([x_4, x_3], S[1])
    x_6 = phi([x_5, x_2], S[0])
    __magma_ssa_return_value_0 = x_6
    O = __magma_ssa_return_value_0
    return O
"""


def test_weird():
    @ssa
    def default(I: m.Bits(2), x_0: m.Bit) -> m.Bit:
        x = I[1]
        if x_0:
            x = I[0]
        return x

    assert inspect.getsource(default) == """\
def default(I: m.Bits(2), x_0: m.Bit) ->m.Bit:
    x_1 = I[1]
    x_2 = I[0]
    x_3 = phi([x_1, x_2], x_0)
    __magma_ssa_return_value_0 = x_3
    O = __magma_ssa_return_value_0
    return O
"""


def test_skip():
    @ssa
    def default(x_0: m.Bit, x_1: m.Bit, x_3: m.Bit) -> m.Bit:
        x = x_1
        if x_0:
            x = x_0
        return x

    assert inspect.getsource(default) == """\
def default(x_0: m.Bit, x_1: m.Bit, x_3: m.Bit) ->m.Bit:
    x_2 = x_1
    x_4 = x_0
    x_5 = phi([x_2, x_4], x_0)
    __magma_ssa_return_value_0 = x_5
    O = __magma_ssa_return_value_0
    return O
"""

# test_wat()
# test_weird()
