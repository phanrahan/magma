from magma.array import Array, ArrayMeta
from magma.bits import Bits


class NDArrayMeta(ArrayMeta):
    def __getitem__(cls, index: tuple):
        if not isinstance(index, tuple):
            raise TypeError("Expected tuple for NDArray parameter")
        if len(index) < 2:
            # For now, only support more than one dimension, otherwise just use
            # an array or bits
            raise ValueError("Invalid number of dimensions")
        for i in index:
            try:
                int(i)
            except (ValueError, TypeError):
                # TODO: For now, we support the traditional Array[N, T]
                # parameter so that the inherited class pipeline works (Array
                # logic), however this interface should not be used by the
                # user, is there a way we can avoid this problem without having
                # to redefine the array core logic? One option might be to
                # factor out the core code from the array type and inherit the
                # generic logic into both
                return super().__getitem__(index)

        # Make inner type
        T = Bits[index[-1]]
        for N in reversed(index[1:-1]):
            T = m.Array[N, T]
        return super().__getitem__((index[0], T))


class NDArray(Array, metaclass=NDArrayMeta):
    def __getitem__(self, index):
        if isinstance(index, tuple):
            result = self
            for i in index:
                result = result[i]
            return result
        return super().__getitem__(index)
