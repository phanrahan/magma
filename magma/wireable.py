from magma.array import Array
from magma.tuple import Tuple
from magma.protocol_type import magma_type


def wireable(T1, T2):
    """
    Returns true if T1 can be wired to T2
    """
    T1, T2 = magma_type(T1), magma_type(T2)
    if issubclass(T1, Tuple):
        if not issubclass(T2, Tuple):
            return False
        return all(wireable(t1, t2) for t1, t2 in zip(T1, T2))
    if issubclass(T1, Array):
        if not issubclass(T2, Array):
            return False
        return wireable(T1.T, T2.T)
    return issubclass(T1, T2) or issubclass(T1, T2)
