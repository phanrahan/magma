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
def basic_if(I_0: m.Bits(2), S_0: m.Bit) ->m.Bit:
    x_0 = I_0[0]
    x_1 = I_0[1]
    x_2 = phi([x_1, x_0], S_0)
    return x_2
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
def basic_if(I_0: m.Bit, S_0: m.Bit) ->m.Bit:
    x_0 = I_0
    x_1 = x_0
    x_2 = x_0
    x_3 = phi([x_2, x_1], S_0)
    return x_3
"""


def test_default():
    @ssa
    def default(I: m.Bits(2), S: m.Bit) -> m.Bit:
        x = I[1]
        if S:
            x = I[0]
        return x

    assert inspect.getsource(default) == """\
def default(I_0: m.Bits(2), S_0: m.Bit) ->m.Bit:
    x_0 = I_0[1]
    x_1 = I_0[0]
    x_2 = phi([x_0, x_1], S_0)
    return x_2
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
def nested(I_0: m.Bits(4), S_0: m.Bits(2)) ->m.Bit:
    x_0 = I_0[0]
    x_1 = I_0[1]
    x_2 = phi([x_1, x_0], S_0[1])
    x_3 = I_0[2]
    x_4 = I_0[3]
    x_5 = phi([x_4, x_3], S_0[1])
    x_6 = phi([x_5, x_2], S_0[0])
    return x_6
"""

def test_weird():
    @ssa
    def default(I: m.Bits(2), x_0: m.Bit) -> m.Bit:
        x = I[1]
        if x_0:
            x = I[0]
        return x

    assert inspect.getsource(default) == """\
def default(I_0: m.Bits(2), x_0_0: m.Bit) ->m.Bit:
    x_0 = I_0[1]
    x_1 = I_0[0]
    x_2 = phi([x_0, x_1], x_0_0)
    return x_2
"""

# test_wat()
# test_weird()
