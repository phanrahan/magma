from types import FunctionType
from collections import Sequence
import inspect
from .bitwise import log2
from .compatibility import StringTypes

__all__ = ['seq2int', 'int2seq', 'ints2seq', 'fun2seq', 'lutinit']


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
            init = (n/nlut) * init
        init = seq2int(init)

    assert n is not None

    return init, n

if __name__ == "__main__":
    def f(a,b):
        return a or b
    print(fun2seq(f))

