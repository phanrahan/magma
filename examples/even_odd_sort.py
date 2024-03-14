import magma as m


class Swap(m.Circuit):
    io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[2]))
    io.O @= m.uncurry(m.fork(m.Bit.And(), m.Bit.Or()))(io.I)
    # Alternative, non-functional version
    # io.O @= m.bits([io.I.reduce_and(), io.I.reduce_or())


class EvenOddSwaps(m.Generator):
    def __init__(self, n: int):
        """n: even integer"""
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        # n // 2 Swap instances, Bits[2] -> Bits[2]
        # join, Array[n // 2, Bits[2]] -> Array[n // 2, Bits[2]]
        # flat, Array[n]
        self.io.O @= m.flat(m.join([Swap() for _ in range(n // 2)]))(self.io.I)


def flatten(l):
    return sum(l, [])


def riffle(n: int):
    return flatten([[i, i + n // 2] for i in range(n // 2)])


def inverse(l):
    return [l.index(i) for i in range(len(l))]


def _unriffle(n: int):
    return inverse(riffle(n))


class Permute(m.Generator2):
    def __init__(self, permutation: list[int]):
        n = len(permutation)
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
