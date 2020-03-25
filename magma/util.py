from magma.array import Array
from magma.bit import Bit
from magma.bits import Bits
from magma.tuple import Tuple


def BitOrBits(width):
    if width is None:
        return Bit
    if not isinstance(width, int):
        raise ValueError(f"Expected width to be None or int, got {width}")
    return Bits[width]


def pretty_str(t):
    if issubclass(t, Tuple):
        args = []
        for i in range(len(t)):
            key_str = str(list(t.keys())[i])
            val_str = pretty_str(list(t.types())[i])
            indent = " " * 4
            val_str = f"\n{indent}".join(val_str.splitlines())
            args.append(f"{key_str} = {val_str}")
        # Pretty print by using newlines + indent
        joiner = ",\n    "
        result = joiner.join(args)
        # Insert first newline + indent and last newline
        result = "\n    " + result + "\n"
        s = f"Tuple({result})"
    elif issubclass(t, Bits):
        s = str(t)
    elif issubclass(t, Array):
        s = f"Array[{t.N}, {pretty_str(t.T)}]"
    else:
        s = str(t)
    return s


def pretty_print_type(t):
    print(pretty_str(t))
