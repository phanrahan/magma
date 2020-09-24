from functools import wraps

import hwtypes as ht

from magma.protocol_type import MagmaProtocol
from magma.debug import debug_info


def python_to_magma_coerce(value):
    if isinstance(value, debug_info):
        # Short circuit tuple converion
        return value

    # Circular import
    from magma.conversions import tuple_, sint, uint, bits, bit
    if isinstance(value, tuple):
        return tuple_(value)
    if isinstance(value, ht.SIntVector):
        return sint(value, len(value))
    if isinstance(value, ht.UIntVector):
        return uint(value, len(value))
    if isinstance(value, ht.BitVector):
        return bits(value, len(value))
    if isinstance(value, (bool, ht.Bit)):
        return bit(value)

    if isinstance(value, MagmaProtocol):
        return value._get_magma_value_()

    return value


def python_to_magma_coerce_wrapper(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        args = (python_to_magma_coerce(a) for a in args)
        kwargs = {k: python_to_magma_coerce(v) for k, v in kwargs.items()}
        return fn(*args, **kwargs)
    return wrapper
