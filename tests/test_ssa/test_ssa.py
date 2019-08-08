import magma as m
from magma.ssa import ssa
from hwtypes import Bit, BitVector
import inspect
import re

import pytest


def test_basic():
    @ssa()
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            x = I[0]
        else:
            x = I[1]
        return x

    assert inspect.getsource(basic_if) == """\
def basic_if(I_0: m.Bits[2], S_0: m.Bit) ->m.Bit:
    x_0 = I_0[0]
    x_1 = I_0[1]
    x_2 = phi([x_1, x_0], S_0)
    __magma_ssa_return_value_0 = x_2
    O = __magma_ssa_return_value_0
    return O
"""


def test_wat():
    @ssa()
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
    __magma_ssa_return_value_0 = x_3
    O = __magma_ssa_return_value_0
    return O
"""


def test_default():
    @ssa()
    def default(I: m.Bits[2], S: m.Bit) -> m.Bit:
        x = I[1]
        if S:
            x = I[0]
        return x

    assert inspect.getsource(default) == """\
def default(I_0: m.Bits[2], S_0: m.Bit) ->m.Bit:
    x_0 = I_0[1]
    x_1 = I_0[0]
    x_2 = phi([x_0, x_1], S_0)
    __magma_ssa_return_value_0 = x_2
    O = __magma_ssa_return_value_0
    return O
"""


def test_nested():
    @ssa()
    def nested(I: m.Bits[4], S: m.Bits[2]) -> m.Bit:
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
def nested(I_0: m.Bits[4], S_0: m.Bits[2]) ->m.Bit:
    x_0 = I_0[0]
    x_1 = I_0[1]
    x_2 = phi([x_1, x_0], S_0[1])
    x_3 = I_0[2]
    x_4 = I_0[3]
    x_5 = phi([x_4, x_3], S_0[1])
    x_6 = phi([x_5, x_2], S_0[0])
    __magma_ssa_return_value_0 = x_6
    O = __magma_ssa_return_value_0
    return O
"""

def test_weird():
    @ssa()
    def default(I: m.Bits[2], x_0: m.Bit) -> m.Bit:
        x = I[1]
        if x_0:
            x = I[0]
        return x

    assert inspect.getsource(default) == """\
def default(I_0: m.Bits[2], x_0_0: m.Bit) ->m.Bit:
    x_0 = I_0[1]
    x_1 = I_0[0]
    x_2 = phi([x_0, x_1], x_0_0)
    __magma_ssa_return_value_0 = x_2
    O = __magma_ssa_return_value_0
    return O
"""


def test_phi_name():
    @ssa(phi='foo')
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            x = I[0]
        else:
            x = I[1]
        return x

    assert inspect.getsource(basic_if) == """\
def basic_if(I_0: m.Bits[2], S_0: m.Bit) ->m.Bit:
    x_0 = I_0[0]
    x_1 = I_0[1]
    x_2 = foo([x_1, x_0], S_0)
    __magma_ssa_return_value_0 = x_2
    O = __magma_ssa_return_value_0
    return O
"""

def test_phi_custom():
    def bar(args, select):
        return 'bar'

    @ssa(phi=bar)
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            x = I[0]
        else:
            x = I[1]
        return x

    assert basic_if([0, 1], 0) == 'bar'

    assert inspect.getsource(basic_if) == """\
def basic_if(I_0: m.Bits[2], S_0: m.Bit) ->m.Bit:
    x_0 = I_0[0]
    x_1 = I_0[1]
    x_2 = __auto_name_0([x_1, x_0], S_0)
    __magma_ssa_return_value_0 = x_2
    O = __magma_ssa_return_value_0
    return O
"""

def test_phi_lambda():
    @ssa(phi=lambda args, s : args[s])
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            x = I[0]
        else:
            x = I[1]
        return x

    assert basic_if([0, 1], 0) == 1

    assert inspect.getsource(basic_if) == """\
def basic_if(I_0: m.Bits[2], S_0: m.Bit) ->m.Bit:
    x_0 = I_0[0]
    x_1 = I_0[1]
    x_2 = __auto_name_0([x_1, x_0], S_0)
    __magma_ssa_return_value_0 = x_2
    O = __magma_ssa_return_value_0
    return O
"""

@pytest.mark.parametrize("i", range(4))
@pytest.mark.parametrize("j", range(4))
@pytest.mark.parametrize("k", range(4))
def test_nested_returns(i, j, k):
    BV = BitVector[2]
    def nest_returns(x: BV, y: BV, z: BV):
        if x[0]:
            if x[1]:
                return y + z
            else:
                return y - z
        else:
            if x[1]:
                return y & z
            else:
                return y | z
    def Not():
        return lambda x : ~x

    nest_returns_ssa = ssa(phi=lambda args, s :s.ite(*args))(nest_returns)
    res = nest_returns(BV(i), BV(j), BV(k))
    res_ssa = nest_returns_ssa(BV(i), BV(j), BV(k))
    assert res == res_ssa

# test_wat()
# test_weird()
