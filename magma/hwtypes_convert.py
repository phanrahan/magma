import magma as m
import hwtypes as ht


def to_hwtypes(T: m.Kind):
    if not isinstance(T, m.Kind):
        raise TypeError("Expected a magma type")
    if issubclass(T, m.Bit):
        return ht.Bit
    elif issubclass(T, m.SInt):
        return ht.SIntVector[T.N]
    elif issubclass(T, m.UInt):
        return ht.UIntVector[T.N]
    elif issubclass(T, m.Bits):
        return ht.BitVector[T.N]
    elif issubclass(T, m.Product):
        _fields = {k: to_hwtypes(v) for k, v in T.field_dict.items()}
        return ht.Product.from_fields(T.__name__, _fields)
    elif issubclass(T, m.Tuple):
        _fields = tuple(to_hwtypes(v) for v in T.fields)
        return ht.Tuple[_fields]
    else:
        raise NotImplementedError(T)
