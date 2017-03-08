from collections import Sequence, OrderedDict
from .ref import TupleRef
from .t import Type, Kind
from .compatibility import IntegerTypes, StringTypes
from .bit import BitOut, VCC, GND

__all__  = ['TupleType', 'TupleKind', 'Tuple']

__all__ += ['tuple_']

#
# Create an Tuple
#
class TupleType(Type):
    def __init__(self, *largs, **kwargs):

        Type.__init__(self, **kwargs)

        if isinstance(largs, Sequence) and len(largs) > 0:
            assert len(largs) == self.N
            self.ts = []
            for i in range(self.N):
                k = self.Ks[i]
                t = largs[i]
                if isinstance(t, IntegerTypes):
                    t = VCC if t else GND
                assert type(t) == self.Ts[i]
                self.ts.append(t)
                setattr(self, k, t)
        else:
            self.ts = []
            for i in range(self.N):
                T = self.Ts[i]
                k = self.Ks[i]
                t = T(name=TupleRef(self,k))
                self.ts.append(t)
                setattr(self, k, t)

    def __eq__(self, rhs):
        if not isinstance(rhs, TupleType): return False
        return self.ts == rhs.ts

    def __getitem__(self, key):
        if key in self.Ks:
            key = self.Ks.index(key)
        return self.ts[key]

    def __len__(self):
        return self.N

    # should I allow this?
    def __call__(self, o):
        return self.wire(o)

    def wire(i, o):
        # print('Tuple.wire(', o, ', ', i, ')')
        
        if not isinstance(o, TupleType):
            print('Wiring error: wiring', o, 'to', i, '(not an Tuple)')
            return

        if i.N != o.N:
            print('Wiring error: Tuples must have the same length', i.N, o.N)
            return

        #if i.Ts != o.Ts:
        #    print('Wiring error: Tuple elements must have the same type')
        #    return

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

    # test whether the values refer a whole tuple
    def iswhole(self, ts):

        for i in range(len(ts)):
            if ts[i].anon():
                #print('not an inst or defn')
                return False

        for i in range(len(ts)):
            # elements must be an tuple reference 
            if not isinstance(ts[i].name, TupleRef):
                #print('not an tuple ref')
                return False

        for i in range(1,len(ts)):
            # elements must refer to the same tuple
            if ts[i].name.tuple is not ts[i-1].name.tuple:
                return False

        for i in range(len(ts)):
            # elements should be numbered consecutively
            if ts[i].name.index != self.Ks[i]:
                return False

        return True


    def trace(self):
        ts = [t.trace() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if len(ts) == self.N and self.iswhole(ts):
            return ts[0].name.tuple

        return tuple_(**dict(zip(self.Ks,ts)))

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if len(ts) == self.N and self.iswhole(ts):
            return ts[0].name.tuple

        return tuple_(**dict(zip(self.Ks,ts)))

class TupleKind(Kind):
    def __init__(cls, name, bases, dct):
        super(TupleKind, cls).__init__(name, bases, dct)
        cls.N = len(cls.Ks)

    def __str__(cls):
        args = []
        for i in range(cls.N):
             args.append("%s=%s" % (cls.Ks[i], str(cls.Ts[i])))
        return "Tuple(%s)" % ",".join(args)

    def __eq__(cls, rhs):
        if not isinstance(rhs, TupleKind): return False

        if cls.Ks != rhs.Ks: return False
        if cls.Ts != rhs.Ts: return False

        return True

    __ne__ = Kind.__ne__
    __hash__ = Kind.__hash__

    def __len__(cls):
        return cls.N

    def __getitem__(cls, key):
        if key in cls.Ks:
            key = cls.Ks.index(key)
        return cls.Ts[key]

    def _isoriented(cls, direction):
        for T in cls.Ts:
            if not T._isoriented(direction):
                return False
        return True

    def qualify(cls, direction):
        if cls._isoriented(direction):
            return cls
        return _Tuple(cls.Ks, [T.qualify(direction) for T in cls.Ts])

    def flip(cls):
        return _Tuple(cls.Ks, [T.flip() for T in cls.Ts])


def _Tuple(Ks, Ts):
    name = 'Tuple(%s)' % ",".join(Ks)
    return TupleKind(name, (TupleType,), dict(Ks=list(Ks), Ts=list(Ts)))
    
def Tuple(*decl, **kwargs):
    n = len(decl)
    if n > 0:
        assert n % 2 == 0
        d = OrderedDict()
        for i in range(0,len(decl),2):
             key, val = decl[i], decl[i+1]
             assert isinstance(key, StringTypes)
             assert isinstance(val, Kind)
             d[key] = val
        return _Tuple(d.keys(), d.values())
    else:
        return _Tuple(kwargs.keys(), kwargs.values())

def tuple_(*larg, **kwargs):
    decl = []
    args = []
    n = len(larg)
    if n > 0:
        assert n % 2 == 0
        for i in range(0, n, 2):
            K = larg[i]
            t = larg[i+1]
            T = type(t)
            if T in IntegerTypes:
                T = BitOut
            decl.append(K)
            decl.append(T)
            args.append(t)
    else:
        for K, t in kwargs.items():
            T = type(t)
            if T in IntegerTypes:
                T = BitOut
            decl.append(K)
            decl.append(T)
            args.append(t)
    return Tuple(*decl)(*args)


if __name__ == '__main__':

    A2 = Tuple('x', Bit, 'y', Bit)
    B2 = Tuple('x', Bit, 'y', Bit)
    print(A2)
    assert A2 == B2
    assert not(A2 != B2)

    a0 = A2(name='a0')
    print(a0)

    a1 = A2(name='a1')
    print(a1)

    print(a1['x'])
    print(a1.x)

    print(tuple_(0,1))

    a1.wire(a0)

    #b0 = a1[0]


