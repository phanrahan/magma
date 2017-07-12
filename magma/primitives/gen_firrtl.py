source = """from magma.circuit import DefineCircuit, EndCircuit
from magma.array import Array
from magma.bit import Bit, In, Out, BitType

def memoize(f):
    memo = {}
    def wrapped(*args):
        if args not in memo:
            memo[args] = f(*args)
        return memo[args]()  # TODO: Should we instance every circuit?
    return wrapped


def type_check_binary_operator(operator):
    \"\"\"
    For Binary Bit operations, the other argument must be a bit
    \"\"\"
    def type_checked_operator(self, other):
        if not isinstance(other, BitType):
            raise TypeError("unsupported operand type(s) for {}: '{}' and"
                    "'{}'".format(operator.__name__, type(self), type(other)))
        return operator(self, other)
    return type_checked_operator
"""

for name, op in [("Add", "add"), ("Sub", "sub"), ("Mul", "mul"), ("Div", "div"), ("Mod", "mod")]:
    source += """
@memoize
def {name}(n):
    circ = DefineCircuit('{name}{{}}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Array(n + 1, Bit)))
    circ.firrtl = "O <= {op}(I0, I1)"
    EndCircuit()
    return circ
""".format(name=name, op=op)

for name, op in [("ULT", "lt"), ("ULE", "leq"), ("UGT", "gt"), ("UGE", "geq"), ("EQ", "eq"), ("NEQ", "neq")]:
    source += """
@memoize
def {name}(n):
    circ = DefineCircuit('{name}{{}}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Bit))
    circ.firrtl = "O <= {op}(I0, I1)"
    EndCircuit()
    return circ
""".format(name=name, op=op)

# Skip padding for now because we can do that in Python instead of at the IR level
# Skip Interpret as {UInt, SInt, Clock} because we are only supporting UInts for now

source += """
@memoize
def ShiftLeft(width, amount):
    circ = DefineCircuit('shl{{}}_{{}}'.format(width, amount), 'I', In(Array(width, Bit)), 'O', Out(Array(width + amount, Bit)))
    circ.firrtl = "O <= shl(I, {{}})"
    EndCircuit()
    return circ
"""

source += """
@memoize
def ShiftRight(width, amount):
    circ = DefineCircuit('shr{{}}_{{}}'.format(width, amount), 'I', In(Array(width, Bit)), 'O', Out(Array(width - amount, Bit)))
    circ.firrtl = "O <= shr(I, {{}})"
    EndCircuit()
    return circ
"""

source += """
@memoize
def DynamicShiftLeft(input_width, shift_amount_width):
    circ = DefineCircuit('dshl{{}}_{{}}'.format(input_width, shift_amount_width), 'I0', In(Array(input_width, Bit)), 'I1', In(Array(shift_amount_width, Bit)), 'O', Out(Array(input_width + 2 ** shift_amount_width - 1, Bit)))
    circ.firrtl = "O <= dshl(I0, I1)"
    EndCircuit()
    return circ
"""

source += """
@memoize
def DynamicShiftRight(input_width, shift_amount_width):
    circ = DefineCircuit('dshr{{}}_{{}}'.format(input_width, shift_amount_width), 'I0', In(Array(input_width, Bit)), 'I1', In(Array(shift_amount_width, Bit)), 'O', Out(Array(input_width, Bit)))
    circ.firrtl = "O <= dshr(I0, I1)"
    EndCircuit()
    return circ
"""

# Skip arithmetic convert to signed operation for now since we are only doing UInts
# Skip negate for now since we are only doing UInts


source += """
@memoize
def Not(n):
    circ = DefineCircuit('not{}'.format(n), 'I', In(Array(n, Bit)), 'O', Out(Array(n, Bit)))
    circ.firrtl = "O <= not(I)"
    EndCircuit()
    return circ
"""

for name, op, bit_method in [("And", "and", "__and__"), ("Or", "or", "__or__"), ("Xor", "xor", "__xor__")]:
    source += """
@memoize
def {name}(n):
    circ = DefineCircuit('{name}{{}}'.format(n), 'I0', In(Array(n, Bit)), 'I1', In(Array(n, Bit)), 'O', Out(Array(n, Bit)))
    circ.firrtl = "O <= {op}(I0, I1)"
    EndCircuit()
    return circ

@type_check_binary_operator
def {bit_method}(self, other):
    return {name}(1)(self, other)[0]
BitType.{bit_method} = {bit_method}
""".format(name=name, op=op, bit_method=bit_method)

for name, op in [("AndR", "andr"), ("OrR", "orr"), ("XorR", "xorr")]:
    source += """
@memoize
def {name}(n):
    circ = DefineCircuit('{name}{{}}'.format(n), 'I', In(Array(n, Bit)), 'O', Out(Array(1, Bit)))
    circ.firrtl = "O <= {op}(I)"
    EndCircuit()
    return circ
""".format(name=name, op=op)

# We skip concat because we can do this in Python
# We skip bit extractions because we can do this in Python
# We skip head because we can do this in Python
# We skip tail because we can do this in Python

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "firrtl.py"), "w") as f:
    f.write(source)
