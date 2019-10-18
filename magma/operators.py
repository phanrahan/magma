from magma import Digital, Bit, Bits, UInt, SInt


class MantleImportError(RuntimeError):
    pass


class UndefinedOperatorError(RuntimeError):
    pass


def raise_mantle_import_error_unary(self):
    raise MantleImportError(
        "Operators are not defined until mantle has been imported")


def raise_mantle_import_error_binary(self, other):
    raise MantleImportError(
        "Operators are not defined until mantle has been imported")


def define_raise_undefined_operator_error(type_str, operator, type_):
    if type_ == "unary":
        def wrapped(self):
            raise UndefinedOperatorError(
                f"{operator} is undefined for {type_str}")
    else:
        assert type_ == "binary"

        def wrapped(self, other):
            raise UndefinedOperatorError(
                f"{operator} is undefined for {type_str}")
    return wrapped


for op in ("__eq__", "__ne__"):
    setattr(Digital, op, raise_mantle_import_error_binary)

for op in (
           "__and__",
           "__or__",
           "__xor__",
           "__invert__",
           "__add__",
           "__sub__",
           "__mul__",
           "__div__",
           "__lt__",
           # __le__ skipped because it's used for assignment on inputs
           # "__le__", 
           "__gt__",
           "__ge__"
           ):
    if op == "__invert__":
        setattr(Digital, op,
                define_raise_undefined_operator_error("Digital", op, "unary"))
    else:
        setattr(
            Digital, op,
            define_raise_undefined_operator_error("Digital", op, "binary"))


for op in ("__and__",
           "__or__",
           "__xor__",
           "__invert__"
           ):
    if op == "__invert__":
        setattr(Bit, op, raise_mantle_import_error_unary)
    else:
        setattr(Bit, op, raise_mantle_import_error_binary)


for op in ("__and__",
           "__or__",
           "__xor__",
           "__invert__",
           "__lshift__",
           "__rshift__",
           ):
    if op == "__invert__":
        setattr(Bits, op, raise_mantle_import_error_unary)
    else:
        setattr(Bits, op, raise_mantle_import_error_binary)

for op in ("__add__",
           "__sub__",
           "__mul__",
           "__div__",
           "__lt__",
           # __le__ skipped because it's used for assignment on inputs
           # "__le__",
           "__gt__",
           "__ge__"
           ):
    setattr(Bits, op,
            define_raise_undefined_operator_error("Bits", op, "binary"))

for op in ("__add__",
           "__sub__",
           "__mul__",
           "__div__",
           "__lt__",
           # __le__ skipped because it's used for assignment on inputs
           # "__le__",
           "__gt__",
           "__ge__"
           ):
    setattr(SInt, op, raise_mantle_import_error_binary)
    setattr(UInt, op, raise_mantle_import_error_binary)
