from collections.abc import Sequence, Mapping
from collections import OrderedDict
from hwtypes.adt import TupleMeta, Tuple, Product, ProductMeta
from hwtypes.util import TypedProperty, OrderedFrozenDict
import magma as m
from .ref import AnonRef, TupleRef
from .t import Type, Kind, Direction, deprecated
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

class TupleKind(TupleMeta, Kind):
    def qualify(cls, direction):
        new_fields = []
        for T in cls.fields:
            new_fields.append(T.qualify(direction))
        return cls.unbound_t[new_fields]

    def flip(cls):
        new_fields = []
        for T in cls.fields:
            new_fields.append(T.flip())
        return cls.unbound_t[new_fields]

    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args)
        obj.__init__(*args, **kwargs)
        return obj

    @property
    def N(cls):
        return len(cls)


class Tuple(Type, Tuple, metaclass=TupleKind):
    def __init__(self, *largs, **kwargs):

        Type.__init__(self, **kwargs) # name=

        self.ts = []
        if len(largs) > 0:
            assert len(largs) == len(self)
            for k, t, T in zip(self.keys(), largs, self.types()):
                if type(t) is bool:
                    t = VCC if t else GND
                self.ts.append(t)
                if not isinstance(self, Product):
                    setattr(self, k, t)
        else:
            for k, T in zip(self.keys(), self.types()):
                t = T(name=TupleRef(self, k))
                self.ts.append(t)
                if not isinstance(self, Product):
                    setattr(self, k, t)

    __hash__ = Type.__hash__

    @classmethod
    def is_oriented(cls, direction):
        return all(v.is_oriented(direction) for v in cls.fields)

    @classmethod
    @deprecated
    def isoriented(cls, direction):
        return cls.is_oriented(direction)

    @classmethod
    def keys(cls):
        return [str(i) for i in range(len(cls.fields))]

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
            key = list(self.keys()).index(key)
        return self.ts[key]

    def __len__(self):
        return len(type(self).fields)

    @classmethod
    def flat_length(cls):
        return sum(T.flat_length() for T in cls.types())

    def __call__(self, o):
        return self.wire(o, get_callee_frame_info())


    @debug_wire
    def wire(i, o, debug_info):
        # print('Tuple.wire(', o, ', ', i, ')')

        if not isinstance(o, Tuple):
            report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because {o.debug_name} is not a Tuple', debug_info)  # noqa
            return

        if i.keys() != o.keys():
            report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}, keys={list(i.keys())}) to {i.debug_name} (type={type(i)}, keys={list(o.keys())}) because the tuples do not have the same keys', debug_info)  # noqa
            return

        #if i.Ts != o.Ts:
        #    print('Wiring error: Tuple elements must have the same type')
        #    return

        for i_elem, o_elem in zip(i, o):
            if o_elem.is_input():
                o_elem.wire(i_elem, debug_info)
            else:
                i_elem.wire(o_elem, debug_info)

    def unwire(i, o):
        for i_elem, o_elem in zip(i, o):
            if o_elem.is_input():
                o_elem.unwire(i_elem, debug_info)
            else:
                i_elem.unwire(o_elem, debug_info)

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
            if ts[i].name.index != list(self.keys())[i]:
                return False

        if len(ts) != len(ts[0].name.tuple):
            # elements should refer to a whole tuple
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

    @classmethod
    def types(cls):
        return cls.fields

    def values(self):
        return self.ts

    def items(self):
        return zip(self.keys(), self.ts)


class ProductKind(ProductMeta, TupleKind, Kind):
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

    def qualify(cls, direction):
        new_fields = OrderedDict()
        for k, v in cls.field_dict.items():
            new_fields[k] = v.qualify(direction)
        return cls.unbound_t.from_fields(cls.__name__, new_fields,
                                         cache=cls.is_cached)

    def flip(cls):
        new_fields = OrderedDict()
        for k, v in cls.field_dict.items():
            new_fields[k] = v.flip()
        return cls.unbound_t.from_fields(cls.__name__, new_fields,
                                         cache=cls.is_cached)

    def __eq__(cls, rhs):
        if not isinstance(rhs, ProductKind):
            return False

        if not cls.is_bound:
            return not rhs.is_bound

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
        return cls.field_dict.keys()

    @classmethod
    def types(cls):
        return cls.fields


from .bitutils import int2seq
from .array import Array
from .bit import Digital, Bit, VCC, GND

#
# convert value to a tuple
#   *value = tuple from positional arguments
#   **kwargs = tuple from keyword arguments
#
def tuple_(value, n=None, t=Tuple):
    if isinstance(value, t):
        return value

    if not isinstance(value, (Digital, Array, IntegerTypes, Sequence, Mapping)):
        raise ValueError(
            "bit can only be used on a Bit, an Array, or an int; not {}".format(type(value)))

    decl = OrderedDict()
    args = []

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(),1)
        value = int2seq(value, n)
    elif isinstance(value, Digital):
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
    for a, d in zip(args, decl):
        # bool types to Bit
        if decl[d] is bool:
            decl[d] = m.Digital
        # Promote integer types to Bits
        elif decl[d] in IntegerTypes:
            decl[d] = m.Bits[max(a.bit_length(), 1)]

    return type("anon", (t,), decl)(*args)


def namedtuple(**kwargs):
    return tuple_(kwargs, t=Product)
