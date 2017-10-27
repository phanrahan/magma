from magma import BitType, BitsType, UIntType, SIntType

class OperatorMantleNotImportedError(RuntimeError):
    def __init__(self):
        self.message = "Operator overloading not activated, please import mantle to use this feature"

def default(self, other):
    raise OperatorMantleNotImportedError()

def unary_default(self):
    raise OperatorMantleNotImportedError()

unary_ops = [
    "__invert__"
]

for op in unary_ops:
    setattr(BitType, op, unary_default)
    setattr(BitsType, op, unary_default)

bitwise_ops = [
    "__and__",
    "__or__",
    "__xor__",
    "__eq__"
]

for op in bitwise_ops:
    setattr(BitType, op, default)
    setattr(BitsType, op, default)

shift_ops = [
    "__lshift__",
    "__rshift__",
]

for op in shift_ops:
    setattr(BitsType, op, default)

arithmetic_ops = [
    "__add__",
    "__sub__",
    "__mul__",
    "__div__"
]

relational_ops = [
    "__lt__",
    "__le__",
    "__gt__",
    "__ge__",
]

for op in arithmetic_ops + relational_ops:
    setattr(UIntType, op, default)
    setattr(SIntType, op, default)
