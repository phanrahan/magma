from hwtypes.bit_vector_abc import TypeFamily
import magma as m


_Family_ = None


def get_family():
    global _Family_
    if _Family_ is None:
        _Family_ = TypeFamily(m.Bit, m.Bits, m.UInt, m.SInt)
    return _Family_
