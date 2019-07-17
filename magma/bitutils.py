# https://wiki.python.org/moin/BitManipulation
# https://code.google.com/p/python-bitstring/
from types import FunctionType
from collections.abc import Sequence
import inspect
from .compatibility import StringTypes

__all__  = ['seq2int', 'int2seq', 'ints2seq', 'fun2seq', 'lutinit']
__all__ += ['int2uint', 'clz', 'pow2', 'log2', 'clog2', 'rol', 'ror']

#
# seq to int
#
def seq2int(l):
    n = len(l)

    i = 0
    for j in range(n):
        if l[j]:
            i |= 1 << j
    return i

#
# int to seq
#
def int2seq(i, n=0):
    if isinstance(i, StringTypes):
        i = ord(i)

    # find minimum number of bits needed for i
    if n == 0:
        j = i
        while j:
            n += 1
            j >>= 1

    return [1 if i & (1 << j) else 0 for j in range(n)]

#
# ints to seq
#
def ints2seq(l, n):
    return [int2seq(i,n) for i in l]

#
# fun to seq
#
def fun2seq(f, n=None):
    if not n:
        logn = len(inspect.getargspec(f).args)
        n = 1 << logn
    else:
        logn = log2(n)
    
    l = []
    for i in range(n):
         arg = int2seq(i, logn)
         l.append(1 if f(*arg) else 0)
    return l

def lutinit(init, n=None):
    if isinstance(init, FunctionType):
        init = fun2seq(init, n)

    if isinstance(init, Sequence):
        nlut = len(init)
        if n != nlut:
            assert n % nlut == 0
            init = (n//nlut) * init
        init = seq2int(init)

    assert n is not None

    return init, n


def int2uint(x, nbits):
    return x & ((1 << nbits)-1)

# base 32
def clz(x):
    if x == 0:
        return 32

    n = 0
    if x <= 0x0000FFFF:
        n = n + 16
        x = x << 16
    if x <= 0x00FFFFFF:
        n = n + 8
        x = x << 8
    if x <= 0x0FFFFFFF:
        n = n + 4
        x = x << 4
    if x <= 0x3FFFFFFF:
        n = n + 2
        x = x << 2
    if x <= 0x7FFFFFFF:
        n = n + 1
    return n


def log2(x):
    return 31 - clz(x)

def clog2(x):
    if x == 0: return 0
    y = log2(x)
    if x > (1 << y):
        y = y + 1
    return y

def pow2(n):
    return 1 << n

def rol(l, m):
    n = len(l)
    return l[m:n] + l[0:m]

def ror(l, m):
    n = len(l)
    return l[n-m:n] + l[0:n-m]


if __name__ == "__main__":
    def f(a,b):
        return a or b
    print(fun2seq(f))
