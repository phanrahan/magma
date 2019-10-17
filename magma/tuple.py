from collections.abc import Sequence, Mapping
from collections import OrderedDict
from hwtypes.adt import TupleMeta, Tuple, Product, ProductMeta
from hwtypes.util import TypedProperty, OrderedFrozenDict
from .ref import AnonRef, TupleRef
from .t import Type, Kind
from .compatibility import IntegerTypes
from .bit import BitOut, VCC, GND
from .debug import debug_wire, get_callee_frame_info
from .port import report_wiring_error

#
# Create an Tuple
#
#  Tuple()
#  - creates a new tuple value
#  Tuple(v0, v1, ..., vn)
#  - creates a new tuple value where each field equals vi
#

class Tuple(Type, Tuple, metaclass=TupleMeta):
    def __init__(self, *largs, **kwargs):

        Type.__init__(self, **kwargs) # name=

        self.ts = []
        if len(largs) > 0:
            assert len(largs) == len(self)
            for k, T in zip(self.keys(), largs):
                t = largs[i]
                if isinstance(t, IntegerTypes):
                    t = VCC if t else GND
                assert type(t) == self.types()[i]
                self.ts.append(t)
                setattr(self, k, t)
        else:
            for k, T in zip(self.keys(), self.types()):
                t = T(name=TupleRef(self,k))
                self.ts.append(t)
                if not isinstance(self, Product):
                    setattr(self, k, t)

    __hash__ = Type.__hash__

    @classmethod
    def is_oriented(cls, direction):
        return all(v.is_oriented(direction) for v in cls.fields)

    @classmethod
    def keys(self):
        return [str(i) for i in range(self.fields)]

    def __eq__(self, rhs):
        if not isinstance(rhs, Tuple): return False
        return self.ts == rhs.ts

    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        kts = ['{}={}'.format(k, v) for k, v in zip(self.keys(), ts)]
        return 'tuple(dict({})'.format(', '.join(kts))

    def __getitem__(self, key):
        if key in self.keys():
            key = self.keys().index(key)
        return self.ts[key]

    def __len__(self):
        return len(type(self).fields)

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

        if not isinstance(o, Tuple):
            report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because {o.debug_name} is not a Tuple', debug_info)  # noqa
            return

        if i.keys() != o.keys():
            report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}, keys={i.keys()}) to {i.debug_name} (type={type(i)}, keys={o.keys()}) because the tuples do not have the same keys', debug_info)  # noqa
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
            if ts[i].name.index != self.keys()[i]:
                return False

        return True


    def trace(self):
        ts = [t.trace() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if len(ts) == len(self) and self.iswhole(ts):
            return ts[0].name.tuple

        return tuple_(dict(zip(self.keys(),ts)))

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if len(ts) == len(self) and self.iswhole(ts):
            return ts[0].name.tuple

        return tuple_(dict(zip(self.keys(),ts)))

    def flatten(self):
        return sum([t.flatten() for t in self.ts], [])

    def const(self):
        for t in self.ts:
            if not t.const():
                return False

        return True

    def keys(self):
        return self.keys()

    def types(self):
        return type(self).fields

    def values(self):
        return self.ts

    def items(self):
        return zip(self.keys(), self.ts)


class ProductKind(ProductMeta, Kind):
    __hash__ = type.__hash__

    @classmethod
    def _from_fields(mcs, fields, name, bases, ns, **kwargs):

        def _get_tuple_base(bases):
            for base in bases:
                if not isinstance(base, mcs) and isinstance(base, TupleMeta):
                    return base
                r_base =_get_tuple_base(base.__bases__)
                if r_base is not None:
                    return r_base
            return None

        base = _get_tuple_base(bases)[tuple(fields.values())]
        bases = *bases, base

        # field_name -> tuple index
        idx_table = dict((k, i) for i,k in enumerate(fields.keys()))

        def _make_prop(field_type, idx):
            @TypedProperty(field_type)
            def prop(self):
                return self[idx]

            @prop.setter
            def prop(self, value):
                self[idx] = value

            return prop

        # add properties to namespace
        # build properties
        for field_name, field_type in fields.items():
            assert field_name not in ns
            idx = idx_table[field_name]
            ns[field_name] = _make_prop(field_type, idx)

        # this is all really gross but I don't know how to do this cleanly
        # need to build t so I can call super() in new and init
        # need to exec to get proper signatures
        t = TupleMeta.__new__(mcs, name, bases, ns, **kwargs)

        # not strictly necessary could iterative over class dict finding
        # TypedProperty to reconstruct _field_table_ but that seems bad
        t._field_table_ = OrderedFrozenDict(fields)
        return t

    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args)
        obj.__init__(*args, **kwargs)
        return obj

    def qualify(cls, direction):
        new_cls = cls
        for v in cls.field_dict.values():
            new_cls = new_cls.rebind(v, v.qualify(direction))
        return new_cls

    def __eq__(cls, rhs):
        if not isinstance(rhs, ProductKind):
            return False

        for k, v in cls.field_dict.items():
            if getattr(rhs, k) != v:
                return False

        return True

    def __len__(cls):
        return len(cls.fields)

    def __str__(cls):
        s = "Tuple("
        s += ",".join(f'{k}={str(v)}' for k, v in cls.field_dict.items())
        s += ")"
        return s


class Product(Tuple, metaclass=ProductKind):
    @classmethod
    def keys(cls):
        return [k for k in cls.field_dict.keys()]

    @classmethod
    def types(cls):
        return cls.fields


# class TupleKind(Kind):
#     def __init__(cls, name, bases, dct):
#         super(TupleKind, cls).__init__(name, bases, dct)
#         cls.N = len(cls.Ks)

#     def __str__(cls):
#         args = []
#         for i in range(cls.N):
#              args.append("%s=%s" % (cls.Ks[i], str(cls.Ts[i])))
#         return "Tuple(%s)" % ",".join(args)

#     def __eq__(cls, rhs):
#         if not isinstance(rhs, TupleKind): return False

#         if cls.Ks != rhs.Ks: return False
#         if cls.Ts != rhs.Ts: return False

#         return True

#     __ne__ = Kind.__ne__
#     __hash__ = Kind.__hash__

#     def __len__(cls):
#         return cls.N

#     def __getitem__(cls, key):
#         if key in cls.Ks:
#             key = cls.Ks.index(key)
#         return cls.Ts[key]

#     def size(cls):
#         n = 0
#         for T in cls.Ts:
#             n += T.size()
#         return n

#     def qualify(cls, direction):
#         if cls.isoriented(direction):
#             return cls
#         return Tuple(OrderedDict(zip(cls.Ks, [T.qualify(direction) for T in cls.Ts])))

#     def flip(cls):
#         return Tuple(OrderedDict(zip(cls.Ks, [T.flip() for T in cls.Ts])))


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
# def Tuple(*largs, **kwargs):
#     if largs:
#         if isinstance(largs[0], Kind):
#             Ks = range(len(largs))
#             Ts = largs
#         else:
#             largs = largs[0]
#             if isinstance(largs, Sequence):
#                 Ks = range(len(largs))
#                 Ts = largs
#             elif isinstance(largs, Mapping):
#                 Ks = list(largs.keys())
#                 Ts = list(largs.values())
#             else:
#                 assert False
#     else:
#         Ks = list(kwargs.keys())
#         Ts = list(kwargs.values())

#     # check types and promote integers
#     for i in range(len(Ts)):
#         T = Ts[i]
#         if T in IntegerTypes:
#             T = BitOut
#             Ts[i] = T
#         if not isinstance(T, Kind):
#             raise ValueError(f'Tuples must contain magma types - got {T}')

#     name = 'Tuple(%s)' % ", ".join([f"{k}: {t}" for k, t in zip(Ks, Ts)])
#     return TupleKind(name, (TupleType,), dict(Ks=Ks, Ts=Ts))

from .bitutils import int2seq
from .array import Array
from .bit import Digital, Bit, VCC, GND

#
# convert value to a tuple
#   *value = tuple from positional arguments
#   **kwargs = tuple from keyword arguments
#
def tuple_(value, n=None):
    if isinstance(value, Tuple):
        return value

    if not isinstance(value, (_Bit, Array, IntegerTypes, Sequence, Mapping)):
        raise ValueError(
            "bit can only be used on a Bit, an Array, or an int; not {}".format(type(value)))

    decl = OrderedDict()
    args = []

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(),1)
        value = int2seq(value, n)
    elif isinstance(value, _Bit):
        value = [value]
    elif isinstance(value, Array):
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
