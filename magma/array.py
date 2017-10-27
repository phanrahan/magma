from collections import Sequence
from .logging import error
from .ref import AnonRef, ArrayRef
from .t import Type, Kind
from .compatibility import IntegerTypes
from .bit import Bit, BitOut, VCC, GND, BitType, BitKind
from .bitutils import int2seq
from .debug import debug_wire, get_callee_frame_info

__all__  = ['ArrayType', 'ArrayKind', 'Array']

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

    __hash__ = Type.__hash__

    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'array([{}])'.format(', '.join(ts))


    def __len__(self):
        return self.N

    def __getitem__(self, key):
        if isinstance(key,slice):
            return array([self[i] for i in range(*key.indices(len(self)))])
        else:
            if not (-self.N <= key and key < self.N):
                raise IndexError

            return self.ts[key]

    def __add__(self, other):
        other_len = other.N
        total = self.N + other_len
        res_bits = []
        for i in range(total):
            res_bits.append(self[i] if i < self.N else other[i - self.N])
        return array(res_bits)

    def __call__(self, o):
        return self.wire(o, get_callee_frame_info())

    @classmethod
    def isoriented(cls, direction):
        return cls.T.isoriented(direction)

    def as_list(self):
        return [self[i] for i in range(len(self))]


    @debug_wire
    def wire(i, o, debug_info):
        # print('Array.wire(', o, ', ', i, ')')

        if not isinstance(o, ArrayType):
            error('Wiring Error: wiring {} ({}) to {} ({})'.format(repr(o), type(o), repr(i), type(i)), include_wire_traceback=True)
            return

        if i.N != o.N:
            error('Wiring Error: Arrays must have the same length {} != {}'.format(i.N, o.N), include_wire_traceback=True)
            return

        for k in range(len(i)):
            i[k].wire(o[k], debug_info)

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

        return array(ts)

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if self.iswhole(ts):
            return ts[0].name.array

        return array(ts)

    def const(self):
        for t in self.ts:
            if not t.const():
                return False

        return True

    def flatten(self):
        return sum([t.flatten() for t in self.ts], [])


class ArrayKind(Kind):
    def __init__(cls, name, bases, dct):
        Kind.__init__( cls, name, bases, dct)

    def __str__(cls):
        s = "Array(%d,%s)" % (cls.N, cls.T)
        #if cls.isinput(): s = 'In({})'.format(s)
        #if cls.isoutput(): s = 'Out({})'.format(s)
        #if cls.isinout(): s = 'InOut({})'.format(s)
        return s

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
            return array([cls[i] for i in xrange(*key.indices(len(cls)))])
        else:
            if not (0 <= key and key < cls.N):
                raise IndexError

            return cls.ts[key]

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return Array(cls.N, cls.T.qualify(direction))

    def flip(cls):
        return Array(cls.N, cls.T.flip())


def Array(N,T):
    assert isinstance(N, IntegerTypes)
    assert isinstance(T, Kind)
    name = 'Array(%d,%s)' % (N,str(T))
    return ArrayKind(name, (ArrayType,), dict(N=N, T=T))


from .conversions import array
