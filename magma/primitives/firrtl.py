from magma.circuit import DefineCircuit, EndCircuit
from magma.array import Array, ArrayType
from magma.bit import Bit, In, Out, BitType

def memoize(f):
    memo = {}
    def wrapped(*args):
        if args not in memo:
            memo[args] = f(*args)
        return memo[args]()  # TODO: Should we instance every circuit?
    return wrapped


def type_check_binary_operator(operator):
    """
    For binary operations, the other argument must be the same type
    """
    def type_checked_operator(self, other):
        if type(self) != type(other):
            raise TypeError("unsupported operand type(s) for {}: '{}' and"
                    "'{}'".format(operator.__name__, type(self), type(other)))
        return operator(self, other)
    return type_checked_operator

@memoize
def Add(n):
    circ = DefineCircuit('Add{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Array(n + 1, Bit)))
    circ.firrtl = "O <= add(I0, I1)"
    EndCircuit()
    return circ

@memoize
def Sub(n):
    circ = DefineCircuit('Sub{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Array(n + 1, Bit)))
    circ.firrtl = "O <= sub(I0, I1)"
    EndCircuit()
    return circ

@memoize
def Mul(n):
    circ = DefineCircuit('Mul{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Array(n + 1, Bit)))
    circ.firrtl = "O <= mul(I0, I1)"
    EndCircuit()
    return circ

@memoize
def Div(n):
    circ = DefineCircuit('Div{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Array(n + 1, Bit)))
    circ.firrtl = "O <= div(I0, I1)"
    EndCircuit()
    return circ

@memoize
def Mod(n):
    circ = DefineCircuit('Mod{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Array(n + 1, Bit)))
    circ.firrtl = "O <= mod(I0, I1)"
    EndCircuit()
    return circ

@memoize
def ULT(n):
    circ = DefineCircuit('ULT{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Bit))
    circ.firrtl = "O <= lt(I0, I1)"
    EndCircuit()
    return circ

@memoize
def ULE(n):
    circ = DefineCircuit('ULE{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Bit))
    circ.firrtl = "O <= leq(I0, I1)"
    EndCircuit()
    return circ

@memoize
def UGT(n):
    circ = DefineCircuit('UGT{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Bit))
    circ.firrtl = "O <= gt(I0, I1)"
    EndCircuit()
    return circ

@memoize
def UGE(n):
    circ = DefineCircuit('UGE{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Bit))
    circ.firrtl = "O <= geq(I0, I1)"
    EndCircuit()
    return circ

@memoize
def EQ(n):
    circ = DefineCircuit('EQ{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Bit))
    circ.firrtl = "O <= eq(I0, I1)"
    EndCircuit()
    return circ

@memoize
def NEQ(n):
    circ = DefineCircuit('NEQ{}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Bit))
    circ.firrtl = "O <= neq(I0, I1)"
    EndCircuit()
    return circ

@memoize
def ShiftLeft(width, amount):
    circ = DefineCircuit('shl{{}}_{{}}'.format(width, amount), 'I', In(Array(width, Bit)), 'O', Out(Array(width + amount, Bit)))
    circ.firrtl = "O <= shl(I, {{}})"
    EndCircuit()
    return circ

@memoize
def ShiftRight(width, amount):
    circ = DefineCircuit('shr{{}}_{{}}'.format(width, amount), 'I', In(Array(width, Bit)), 'O', Out(Array(width - amount, Bit)))
    circ.firrtl = "O <= shr(I, {{}})"
    EndCircuit()
    return circ

@memoize
def DynamicShiftLeft(input_width, shift_amount_width):
    circ = DefineCircuit('dshl{{}}_{{}}'.format(input_width, shift_amount_width), 'I0', In(Array(input_width, Bit)), 'I1', In(Array(shift_amount_width, Bit)), 'O', Out(Array(input_width + 2 ** shift_amount_width - 1, Bit)))
    circ.firrtl = "O <= dshl(I0, I1)"
    EndCircuit()
    return circ

@memoize
def DynamicShiftRight(input_width, shift_amount_width):
    circ = DefineCircuit('dshr{{}}_{{}}'.format(input_width, shift_amount_width), 'I0', In(Array(input_width, Bit)), 'I1', In(Array(shift_amount_width, Bit)), 'O', Out(Array(input_width, Bit)))
    circ.firrtl = "O <= dshr(I0, I1)"
    EndCircuit()
    return circ

@memoize
def Not(n):
    circ = DefineCircuit('not{}'.format(n), 'I', In(Array(n, Bit)), 'O', Out(Array(n, Bit)))
    circ.firrtl = "O <= not(I)"
    EndCircuit()
    return circ

@memoize
def And(n):
    if n == 1:
        typ = Bit
    else:
        typ = Array(n, Bit)
    circ = DefineCircuit('And{}'.format(n), 'I0', In(typ), 'I1', In(typ), 'O', Out(typ))
    circ.firrtl = "O <= and(I0, I1)"
    EndCircuit()
    return circ

@type_check_binary_operator
def __and__(self, other):
    return And(1)(self, other)
BitType.__and__ = __and__

@type_check_binary_operator
def __and__(self, other):
    return And(len(self))(self, other)
ArrayType.__and__ = __and__

@memoize
def Or(n):
    if n == 1:
        typ = Bit
    else:
        typ = Array(n, Bit)
    circ = DefineCircuit('Or{}'.format(n), 'I0', In(typ), 'I1', In(typ), 'O', Out(typ))
    circ.firrtl = "O <= or(I0, I1)"
    EndCircuit()
    return circ

@type_check_binary_operator
def __or__(self, other):
    return Or(1)(self, other)
BitType.__or__ = __or__

@type_check_binary_operator
def __or__(self, other):
    return Or(len(self))(self, other)
ArrayType.__or__ = __or__

@memoize
def Xor(n):
    if n == 1:
        typ = Bit
    else:
        typ = Array(n, Bit)
    circ = DefineCircuit('Xor{}'.format(n), 'I0', In(typ), 'I1', In(typ), 'O', Out(typ))
    circ.firrtl = "O <= xor(I0, I1)"
    EndCircuit()
    return circ

@type_check_binary_operator
def __xor__(self, other):
    return Xor(1)(self, other)
BitType.__xor__ = __xor__

@type_check_binary_operator
def __xor__(self, other):
    return Xor(len(self))(self, other)
ArrayType.__xor__ = __xor__

@memoize
def AndR(n):
    circ = DefineCircuit('AndR{}'.format(n), 'I', In(Array(n, Bit)), 'O', Out(Array(1, Bit)))
    circ.firrtl = "O <= andr(I)"
    EndCircuit()
    return circ

@memoize
def OrR(n):
    circ = DefineCircuit('OrR{}'.format(n), 'I', In(Array(n, Bit)), 'O', Out(Array(1, Bit)))
    circ.firrtl = "O <= orr(I)"
    EndCircuit()
    return circ

@memoize
def XorR(n):
    circ = DefineCircuit('XorR{}'.format(n), 'I', In(Array(n, Bit)), 'O', Out(Array(1, Bit)))
    circ.firrtl = "O <= xorr(I)"
    EndCircuit()
    return circ
