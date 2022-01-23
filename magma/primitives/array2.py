"""
Monkey patched functions to avoid circular dependencies in Array2 definitions
"""

from magma.interface import IO
from magma.t import In, Out
from magma.generator import Generator2
from magma.array import Array


class Reverse(Generator2):
    def __init__(self, T):
        self.io = IO(I=In(T), O=Out(T))
        for i in range(T.N):
            self.io.O[T.N - 1 - i] @= self.io.I[i]


Array.reversed = lambda self: Reverse(type(self))()(self)
