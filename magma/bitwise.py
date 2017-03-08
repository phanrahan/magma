# https://wiki.python.org/moin/BitManipulation
# https://code.google.com/p/python-bitstring/

def uint(x, nbits):
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


