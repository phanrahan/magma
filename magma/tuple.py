from collections.abc import Sequence, Mapping
from collections import OrderedDict
from .ref import AnonRef, TupleRef
from .t import Type, Kind
from .compatibility import IntegerTypes
from .bit import BitOut, VCC, GND
from .debug import debug_wire, get_callee_frame_info
from .port import report_wiring_error

__all__  = ['TupleType', 'TupleKind', 'Tuple']

#
# Create an Tuple
#
#  Tuple()
#  - creates a new tuple value
#  Tuple(v0, v1, ..., vn)
#  - creates a new tuple value where each field equals vi
#
class TupleType(Type):
    def __init__(self, *largs, **kwargs):

        Type.__init__(self, **kwargs) # name=

        self.ts = []
        if len(largs) > 0:
            assert len(largs) == self.N
            for i in range(self.N):
                k = str(self.Ks[i])
                t = largs[i]
                if isinstance(t, IntegerTypes):
                    t = VCC if t else GND
                assert type(t) == self.Ts[i]
                self.ts.append(t)
                setattr(self, k, t)
        else:
            for i in range(self.N):
                k = str(self.Ks[i])
                T = self.Ts[i]
                t = T(name=TupleRef(self,k))
                self.ts.append(t)
                setattr(self, k, t)

    __hash__ = Type.__hash__

    def __eq__(self, rhs):
        if not isinstance(rhs, TupleType): return False
        return self.ts == rhs.ts

    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        kts = ['{}={}'.format(k, v) for k, v in zip(self.Ks, ts)]
        return 'tuple(dict({})'.format(', '.join(kts))

    def __getitem__(self, key):
        if key in self.Ks:
            key = self.Ks.index(key)
        return self.ts[key]

    def __len__(self):
        return self.N

    def __call__(self, o):
        return self.wire(o, get_callee_frame_info())

    @classmethod
    def isoriented(cls, direction):
        for T in cls.Ts:
            if not T.isoriented(direction):
                return False
        return True


    @debug_wire
    def wire(i, o, debug_info):
        # print('Tuple.wire(', o, ', ', i, ')')

        if not isinstance(o, TupleType):
            report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because {o.debug_name} is not a Tuple', debug_info)  # noqa
            return

        if i.Ks != o.Ks:
            report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}, keys={i.Ks}) to {i.debug_name} (type={type(i)}, keys={o.Ks}) because the tuples do not have the same keys', debug_info)  # noqa
            return

        #if i.Ts != o.Ts:
        #    print('Wiring error: Tuple elements must have the same type')
        #    return

        for i_elem, o_elem in zip(i, o):
            if o_elem.isinput():
                o_elem.wire(i_elem, debug_info)
            else:
                i_elem.wire(o_elem, debug_info)

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

        return tuple_(dict(zip(self.Ks,ts)))

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if len(ts) == self.N and self.iswhole(ts):
            return ts[0].name.tuple

        return tuple_(dict(zip(self.Ks,ts)))

    def flatten(self):
        return sum([t.flatten() for t in self.ts], [])

    def const(self):
        for t in self.ts:
            if not t.const():
                return False

        return True

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

    def size(cls):
        n = 0
        for T in cls.Ts:
            n += T.size()
        return n

    def qualify(cls, direction):
        if cls.isoriented(direction):
            return cls
        return Tuple(OrderedDict(zip(cls.Ks, [T.qualify(direction) for T in cls.Ts])))

    def flip(cls):
        return Tuple(OrderedDict(zip(cls.Ks, [T.flip() for T in cls.Ts])))


#
# Tuple(Mapping)
# Tuple(Sequence)
#
# *largs with largs being comprised of magma types
#    Tuple(T0, T1, ..., Tn)
#
# **kwargs - only called if largs is empty
#    Tuple(x=Bit, y=Bit) -> Tuple(**kwargs)
#
def Tuple(*largs, **kwargs):
    if largs:
        if isinstance(largs[0], Kind):
            Ks = range(len(largs))
            Ts = largs
        else:
            largs = largs[0]
            if isinstance(largs, Sequence):
                Ks = range(len(largs))
                Ts = largs
            elif isinstance(largs, Mapping):
                Ks = list(largs.keys())
                Ts = list(largs.values())
            else:
                assert False
    else:
        Ks = list(kwargs.keys())
        Ts = list(kwargs.values())

    # check types and promote integers
    for i in range(len(Ts)):
        T = Ts[i]
        if T in IntegerTypes:
            T = BitOut
            Ts[i] = T
        if not isinstance(T, Kind):
            raise ValueError(f'Tuples must contain magma types - got {T}')

    name = 'Tuple(%s)' % ", ".join([f"{k}: {t}" for k, t in zip(Ks, Ts)])
    return TupleKind(name, (TupleType,), dict(Ks=Ks, Ts=Ts))

from .bitutils import int2seq
from .array import ArrayType, Array
from .bit import _BitKind, _BitType, Bit, BitKind, BitType, VCC, GND

#
# convert value to a tuple
#   *value = tuple from positional arguments
#   **kwargs = tuple from keyword arguments
#
def tuple_(value, n=None):
    if isinstance(value, TupleType):
        return value

    if not isinstance(value, (_BitType, ArrayType, IntegerTypes, Sequence, Mapping)):
        raise ValueError(
            "bit can only be used on a Bit, an Array, or an int; not {}".format(type(value)))

    decl = OrderedDict()
    args = []

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(),1)
        value = int2seq(value, n)
    elif isinstance(value, _BitType):
        value = [value]
    elif isinstance(value, ArrayType):
        value = [value[i] for i in range(len(value))]

    if isinstance(value, Sequence):
        ts = list(value)
        for i in range(len(ts)):
            args.append(ts[i])
            decl[i] = type(ts[i])
    elif isinstance(value, Mapping):
        for k, v in value.items():
            args.append(v)
            decl[k] = type(v)

    return Tuple(decl)(*args)


def namedtuple(**kwargs):
    return tuple_(kwargs)
