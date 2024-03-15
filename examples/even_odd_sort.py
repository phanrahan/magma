import magma as m
from typing import Tuple


def is_power_of_two(n):
    return (n & (n - 1) == 0) and n != 0


class Swap(m.Circuit):
    io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[2]))
    io.O @= m.uncurry(m.fork(m.Bit.And(), m.Bit.Or()))(io.I)
    # Alternative, non-functional version
    # io.O @= m.bits([io.I.reduce_and(), io.I.reduce_or())


def swap(I: m.Bits[2]):
    return Swap()(I)


class EvenOddSwaps(m.Generator):
    """Swap adjacent indices"""

    def __init__(self, n: int):
        assert n % 2 == 0, "Expected n to be even"
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        if n > 2:
            x = m.flat(m.join(
                [Swap() for _ in range((n - 2) // 2)]
            ))(self.io.I[1:-1])
            self.io.O[1:-1] @= x
        self.io.O[0] @= self.io.I[0]
        self.io.O[-1] @= self.io.I[-1]


def flatten(t: tuple):
    return sum(t, tuple())


def riffle(n: int):
    assert n % 2 == 0, "Expected n to be even"
    return flatten(tuple((i, i + n // 2) for i in range(n // 2)))


def inverse(t: tuple):
    return tuple(t.index(i) for i in range(len(t)))


def unriffle(n: int):
    return inverse(riffle(n))


class Permute(m.Generator):
    def __init__(self, permutation: Tuple[int]):
        n = len(permutation)
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        self.io.O @= m.bits([self.io.I[i] for i in permutation])


def Riffle(n: int):
    return Permute(riffle(n))


def Unriffle(n: int):
    return Permute(unriffle(n))


class EvenOddMerger(m.Generator):
    def __init__(self, n: int):
        self.name = f'EvenOddMerger{n}'
        assert is_power_of_two(n)
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        if n == 2:
            self.io.O @= swap(self.io.I)
            return
        even_merger = EvenOddMerger(n // 2)()
        odd_merger = EvenOddMerger(n // 2)()
        merger = m.flat(m.join(even_merger, odd_merger))
        sorter = m.compose(EvenOddSwaps(n)(),
                           Riffle(n)(),
                           merger,
                           Unriffle(n)())
        self.io.O @= sorter(self.io.I)


class EvenOddSorter(m.Generator):
    def __init__(self, n: int):
        # TODO: update fault to emit names after uniquification
        self.name = f'EvenOddSorter{n}'
        assert is_power_of_two(n)
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        if n == 1:
            self.io.O @= self.io.I
            return
        bot_sorter = EvenOddSorter(n // 2)()
        top_sorter = EvenOddSorter(n // 2)()
        sorter = m.flat(m.join(bot_sorter, top_sorter))
        merger = EvenOddMerger(n)()
        self.io.O @= m.compose(merger, sorter)(self.io.I)
