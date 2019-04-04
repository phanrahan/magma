from collections import Sequence
from .bitutils import int2seq
from .ref import AnonRef, ArrayRef
from .t import Type, Kind
from .compatibility import IntegerTypes
from .bit import VCC, GND
from .bitutils import seq2int
from .debug import debug_wire, get_callee_frame_info
from .port import report_wiring_error
import weakref

__all__ = ['ArrayType', 'ArrayKind', 'Array']


class ArrayKind(Kind):
    _class_cache = weakref.WeakValueDictionary()
    def __init__(cls, name, bases, dct):
        Kind.__init__(cls, name, bases, dct)

    def __str__(cls):
        return "Array[%d, %s]" % (cls.N, cls.T)

    def __getitem__(cls, index):
        width, sub_type = index
        try:
            return ArrayKind._class_cache[width, sub_type]
        except KeyError:
            pass
        bases = [cls]
        bases = tuple(bases)
        class_name = '{}[{}, {}]'.format(cls.__name__, width, sub_type.__name__)
        t = type(cls)(class_name, bases, dict(N=width, T=sub_type))
        t.__module__ = cls.__module__
        ArrayKind._class_cache[width, sub_type] = t
        return t

    def __eq__(cls, rhs):
        if not issubclass(type(rhs), ArrayKind):
            return False

        if cls.N != rhs.N:
            return False
        if cls.T != rhs.T:
            return False

        return True

    __ne__ = Kind.__ne__
    __hash__ = Kind.__hash__

    def __len__(cls):
        return cls.N

#     def __getitem__(cls, key):
#         if isinstance(key, slice):
#             return array([cls[i] for i in range(*key.indices(len(cls)))])
#         else:
#             if not (0 <= key and key < cls.N):
#                 raise IndexError

#             return cls.ts[key]

    def size(cls):
        return cls.N * cls.T.size()

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return Array[cls.N, cls.T.qualify(direction)]

    def flip(cls):
        return Array[cls.N, cls.T.flip()]

    def __call__(cls, *args, **kwargs):
        result = super().__call__(*args, **kwargs)
        if len(args) == 1 and isinstance(args[0], Array) and not \
                (issubclass(cls.T, Array) and cls.N == 1):
            arg = args[0]
            if len(arg) < len(result):
                from .conversions import zext
                arg = zext(arg, len(result) - len(arg))
            result(arg)
        return result


class Array(Type, metaclass=ArrayKind):
    def __init__(self, *largs, **kwargs):

        Type.__init__(self, **kwargs)

        if isinstance(largs, Sequence) and len(largs) == self.N:
            self.ts = []
            for t in largs:
                if isinstance(t, IntegerTypes):
                    t = VCC if t else GND
                assert type(t) == self.T, (type(t), self.T)
                self.ts.append(t)
        elif len(largs) == 1 and isinstance(largs[0], int):
            self.ts = []
            for bit in int2seq(largs[0], self.N):
                self.ts.append(VCC if bit else GND)
        elif len(largs) == 1 and isinstance(largs[0], Array):
            assert len(largs[0]) <= self.N
            T = self.T
            self.ts = list(type(t)() for t in largs[0])
            if len(largs[0]) < self.N:
                self.ts += [self.T() for _ in range(self.N - len(largs[0]))]
        elif len(largs) == 1 and isinstance(largs[0], list):
            assert len(largs[0]) <= self.N
            T = self.T
            self.ts = largs[0][:]
            if len(largs[0]) < self.N:
                self.ts += [self.T() for _ in range(self.N - len(largs[0]))]
        else:
            self.ts = []
            for i in range(self.N):
                T = self.T
                t = T(name=ArrayRef(self, i))
                self.ts.append(t)

    def __eq__(self, rhs):
        if not isinstance(rhs, ArrayType):
            return False
        return self.ts == rhs.ts

    __hash__ = Type.__hash__

    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'array([{}])'.format(', '.join(ts))

    def __len__(self):
        return self.N

    def __getitem__(self, key):
        if isinstance(key, ArrayType) and all(t in {VCC, GND} for t in key.ts):
            key = seq2int([0 if t is GND else 1 for t in key.ts])
        if isinstance(key, slice):
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
            if isinstance(o, IntegerTypes):
                report_wiring_error(f'Cannot wire {o} (type={type(o)}) to {i.debug_name} (type={type(i)}) because conversions from IntegerTypes are only defined for Bits, not general Arrays', debug_info)  # noqa
            else:
                report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because {o.debug_name} is not an Array', debug_info)  # noqa
            return

        if i.N != o.N:
            report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because the arrays do not have the same length', debug_info)  # noqa
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
                return False

        for i in range(n):
            # elements must be an array reference
            if not isinstance(ts[i].name, ArrayRef):
                return False

        for i in range(1, n):
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


# def Array(N, T):
#     assert isinstance(N, IntegerTypes)
#     assert isinstance(T, Kind)
#     name = 'Array(%d,%s)' % (N, str(T))
#     return ArrayKind(name, (ArrayType,), dict(N=N, T=T))

ArrayType = Array


# Workaround for circular dependency
from .conversions import array  # nopep8
