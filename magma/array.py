from collections import Sequence
from .error import error
from .ref import ArrayRef
from .t import Type, Kind
from .compatibility import IntegerTypes
from .bit import Bit, BitOut, VCC, GND 
from .bits import int2seq

__all__  = ['ArrayType', 'ArrayKind', 'Array']

__all__ += ['Array1', 'Array2', 'Array3', 'Array4']
__all__ += ['Array5', 'Array6', 'Array7', 'Array8']
__all__ += ['Array9', 'Array10', 'Array11', 'Array12']
__all__ += ['Array13', 'Array14', 'Array15', 'Array16']
__all__ += ['Array18']

__all__ += ['array', 'concat', 'constarray']

#
# Create an Array
#
class ArrayType(Type):
    def __init__(self, *largs, **kwargs):

        Type.__init__(self, **kwargs)

        if isinstance(largs, Sequence) and len(largs) > 0:
            assert len(largs) == self.N
            self.ts = []
            for t in largs:
                if isinstance(t, IntegerTypes):
                    t = VCC if t else GND
                assert type(t) == self.T
                self.ts.append(t)
        else:
            self.ts = []
            for i in range(self.N):
                T = self.T
                t = T(name=ArrayRef(self,i))
                self.ts.append(t)

    def __eq__(self, rhs):
        if not isinstance(rhs, ArrayType): return False
        return self.ts == rhs.ts

    def __len__(self):
        return self.N

    def __getitem__(self, key):
        if isinstance(key,slice):
            return array(*[self[i] for i in range(*key.indices(len(self)))])
        else:
            assert 0 <= key and key < self.N, "key: %d, self.N: %d" %(key,self.N)
            return self.ts[key]

    def __add__(self, other):
        other_len = other.N
        total = self.N + other_len
        res_bits = []
        for i in range(total):
            res_bits.append(self[i] if i < self.N else other[i - self.N])
        return array(*res_bits)

    # should I allow this?
    def __call__(self, o):
        return self.wire(o)

    def wire(i, o):
        # print('Array.wire(', o, ', ', i, ')')
        
        if not isinstance(o, ArrayType):
            error('Wiring Error: wiring {} to {} (not an Array)'.format(o, i))
            return

        #if i.T != o.T:
        #    print('Wiring error: Array elements must have the same type')
        #    return

        if i.N != o.N:
            error('Wiring Error: Arrays must have the same length {} != {}'.format(i.N, o.N))
            return 

        for k in range(len(i)):
            i[k].wire(o[k])

    def driven(self):
        for t in self.ts:
            if not t.driven():
                return False
        return True

    def wired(self):
        for t in self.ts:
            if not t.wired():
                return False
        return True

    # test whether the values refer a whole array
    def iswhole(self, ts):

        n = len(ts)

        for i in range(n):
            if ts[i].anon():
                #print('not an inst or defn')
                return False

        for i in range(n):
            # elements must be an array reference 
            if not isinstance(ts[i].name, ArrayRef):
                #print('not an array ref')
                return False

        for i in range(1,n):
            # elements must refer to the same array
            if ts[i].name.array is not ts[i-1].name.array:
                return False

        if n > 0 and n != ts[0].name.array.N:
            # must use all of the elements of the base array 
            return False

        for i in range(n):
            # elements should be numbered consecutively
            if ts[i].name.index != i:
                return False

        return True


    def trace(self):
        ts = [t.trace() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if self.iswhole(ts):
            return ts[0].name.array

        return array(*ts)

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if self.iswhole(ts):
            return ts[0].name.array

        return array(*ts)

class ArrayKind(Kind):
    def __init__(cls, name, bases, dct):
        Kind.__init__( cls, name, bases, dct)

    def __str__(cls):
        return "Array(%d,%s)" % (cls.N, cls.T)

    def __eq__(cls, rhs):
        if not isinstance(rhs, ArrayKind): return False

        if cls.N != rhs.N: return False
        if cls.T != rhs.T: return False

        return True

    __ne__ = Kind.__ne__
    __hash__ = Kind.__hash__

    def __len__(cls):
        return cls.N

    def __getitem__(cls, key):
        if isinstance(key,slice):
            return array(*[cls[i] for i in xrange(*key.indices(len(cls)))])
        else:
            assert 0 <= key and key < cls.N
            return cls.ts[key]

    def _isoriented(cls, direction):
        return cls.T._isoriented(direction)

    def qualify(cls, direction):
        if cls.T._isoriented(direction):
            return cls
        return Array(cls.N, cls.T.qualify(direction))

    def flip(cls):
        return Array(cls.N, cls.T.flip())


def Array(N,T):
    assert isinstance(N, IntegerTypes)
    assert isinstance(T, Kind)
    name = 'Array(%d,%s)' % (N,str(T))
    return ArrayKind(name, (ArrayType,), dict(N=N, T=T))

Array1 = Array(1,Bit)
Array2 = Array(2,Bit)
Array3 = Array(3,Bit)
Array4 = Array(4,Bit)
Array5 = Array(5,Bit)
Array6 = Array(6,Bit)
Array7 = Array(7,Bit)
Array8 = Array(8,Bit)
Array9 = Array(9,Bit)
Array10 = Array(10,Bit)
Array11 = Array(11,Bit)
Array12 = Array(12,Bit)
Array13 = Array(13,Bit)
Array14 = Array(14,Bit)
Array15 = Array(15,Bit)
Array16 = Array(16,Bit)

Array18 = Array(18,Bit)

def array(*ts):

    # create list of types
    Ts = []
    for t in ts:
        T = type(t)
        if T in IntegerTypes:
            T = BitOut
        Ts.append(T)

    # check that they are all the same
    for t in Ts:
       assert t == T

    return Array(len(Ts), T)(*ts)

def constarray(i, n):
    return array(*int2seq(i, n))

def concat(*arrays):
    ts = [t for a in arrays for t in a.ts] # flatten
    return array(*ts)
    
if __name__ == '__main__':
    from magma.port import INPUT, OUTPUT, INOUT

    A2 = Array(2,Bit)
    B2 = Array(2,Bit)
    print(A2)
    assert A2 == B2
    assert not(A2 != B2)

    A4 = Array(4,Bit)
    print(A4)
    assert A4 == Array4
    assert A2 != A4

    A24 = Array(2,A4)
    print(A24)
    assert A2 != A4

    a0 = Array4(name='a0',direction=OUTPUT)
    print(a0)

    print(str(a0.ts[0]))

    a1 = Array4(name='a1',direction=INPUT)
    print(a1)

    #a1.wire(a0)
    #print(a1.lvalue(), a1.value())

    #b0 = a1[0]
    #print(b0.lvalue(), b0.value())

    #a3 = a1[0:2]
    #print(a3.lvalue(), a3.value())

