"""
Batcher odd–even mergesort sorting network

Useful references:
* https://hwlang.de/algorithmen/sortieren/networks/oemen.htm
* https://cs.wmich.edu/gupta/teaching/cs5260/5260Sp15web/lectureNotes/Odd-even%20mergesort%20basics.pdf
"""

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


class OddEvenSwaps(m.Generator):
    """Swap adjacent indices for [1:-2]"""

    def __init__(self, n: int):
        assert n % 2 == 0, "Expected n to be even"
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        if n > 2:
            self.io.O[1:-1] @= m.flat(
                m.join([Swap() for _ in range(n // 2 - 1)])
            )(self.io.I[1:-1])
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


class OddEvenMerger(m.Generator):
    def __init__(self, n: int):
        self.name = f'OddEvenMerger{n}'
        assert is_power_of_two(n)
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        if n == 2:
            self.io.O @= swap(self.io.I)
            return
        sorter = m.compose(OddEvenSwaps(n)(),
                           Riffle(n)(),
                           m.flat(m.join(OddEvenMerger(n // 2)(),
                                         OddEvenMerger(n // 2)())),
                           Unriffle(n)())
        self.io.O @= sorter(self.io.I)


class OddEvenSorter(m.Generator):
    def __init__(self, n: int):
        # NOTE(leonardt): need explicit name due to fault issue
        # https://github.com/leonardt/fault/issues/338
        self.name = f'OddEvenSorter{n}'
        assert is_power_of_two(n)
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        if n == 1:
            self.io.O @= self.io.I
            return
        sorter = m.compose(OddEvenMerger(n)(),
                           m.flat(m.join(OddEvenSorter(n // 2)(),
                                         OddEvenSorter(n // 2)())))
        self.io.O @= sorter(self.io.I)
