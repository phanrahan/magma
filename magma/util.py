from magma.array import Array
from magma.bit import Bit
from magma.bits import Bits
from magma.tuple import Tuple
from magma import clear_cachedFunctions

from magma.frontend import coreir_
from magma.generator import reset_generator_cache
from magma.logging import flush_all
from magma.when import reset_context as reset_when_context


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


def reset_global_context():
    """
    Add this to your conftest.py to reset the magma compiler between tests

    Should also be used in between multiple calls of m.compile to reset the
    compiler's state
    """
    clear_cachedFunctions()
    coreir_.ResetCoreIR()
    reset_generator_cache()
    flush_all()  # flush all staged logs
    reset_when_context()
