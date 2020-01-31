import itertools
from collections.abc import Sequence, Mapping
from collections import OrderedDict
from hwtypes.adt import TupleMeta, Tuple as Tuple_, Product, ProductMeta
from hwtypes.adt_meta import BoundMeta, RESERVED_SUNDERS
from hwtypes.util import TypedProperty, OrderedFrozenDict
import magma as m
from .common import deprecated
from .ref import AnonRef, TupleRef
from .t import Type, Kind, Direction
from .compatibility import IntegerTypes
from .bit import BitOut, VCC, GND
from .debug import debug_wire, get_callee_frame_info
from .logging import root_logger


_logger = root_logger()


#
# Create an Tuple
#
#  Tuple()
#  - creates a new tuple value
#  Tuple(v0, v1, ..., vn)
#  - creates a new tuple value where each field equals vi
#

class TupleKind(TupleMeta, Kind):
    def __new__(mcs, name, bases, namespace, fields=None, **kwargs):
        for rname in RESERVED_SUNDERS:
            if rname in namespace:
                raise ReservedNameError(f'class attribute {rname} is reserved by the type machinery')

        bound_types = fields
        has_bound_base = False
        unbound_bases = []
        for base in bases:
            if isinstance(base, BoundMeta):
                if base.is_bound:
                    has_bound_base = True
                    if bound_types is None:
                        bound_types = base.fields
                    elif any(not (issubclass(x, y) or issubclass(y, x)) for x,
                             y in zip(bound_types, base.fields)):
                        raise TypeError("Can't inherit from multiple different bound_types")
                else:
                    unbound_bases.append(base)

        t = type.__new__(mcs, name, bases, namespace, **kwargs)
        t._fields_ = bound_types
        t._unbound_base_ = None

        if bound_types is None:
            # t is a unbound type
            t._unbound_base_ = t
        elif len(unbound_bases) == 1:
            # t is constructed from an unbound type
            t._unbound_base_ = unbound_bases[0]
        elif not has_bound_base:
            # this shouldn't be reachable
            raise AssertionError("Unreachable code")

        return t

    def _from_idx(cls, idx):
        # Some of this should probably be in GetitemSyntax
        mcs = type(cls)

        try:
            return mcs._class_cache[cls, idx]
        except KeyError:
            pass

        if cls.is_bound:
            raise TypeError('Type is already bound')

        undirected_idx = tuple(v.qualify(Direction.Undirected) for v in idx)
        if undirected_idx != idx:
            bases = [cls[undirected_idx]]
        else:
            bases = [cls]
        bases = tuple(bases)
        class_name = cls._name_cb(idx)

        t = mcs(class_name, bases, {'__module__' : cls.__module__}, fields=idx)
        if t._unbound_base_ is None:
            t._unbound_base_ = cls
        mcs._class_cache[cls, idx] = t
        t._cached_ = True
        return t

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


class Tuple(Type, Tuple_, metaclass=TupleKind):
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
        if not isinstance(rhs, type(self)):
            return NotImplemented
        else:
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

    def __setitem__(self, key, val):
        old = self[key]
        if old is not val:
            _logger.error(f'May not mutate Tuple, trying to replace '
                          f'{self}[{key}] ({old}) with {val}')

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
            _logger.error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because {o.debug_name} is not a Tuple', debug_info=debug_info)  # noqa
            return

        if i.keys() != o.keys():
            _logger.error(f'Cannot wire {o.debug_name} (type={type(o)}, keys={list(i.keys())}) to {i.debug_name} (type={type(i)}, keys={list(o.keys())}) because the tuples do not have the same keys', debug_info=debug_info)  # noqa
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

    def undriven(self):
        for elem in self:
            elem.undriven()

    def unused(self):
        for elem in self:
            elem.unused()


class ProductKind(ProductMeta, TupleKind, Kind):
    __hash__ = type.__hash__

    def __new__(mcs, name, bases, namespace, cache=True, **kwargs):
        return super().__new__(mcs, name, bases, namespace, cache, **kwargs)

    def from_fields(cls, name, fields , cache=True):
        return super().from_fields(name, fields, cache)

    @classmethod
    def _from_fields(mcs, fields, name, bases, ns, **kwargs):

        cls = bases[0]

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
            if field_name == "N":
                # TODO: Make N unreserved
                raise ValueError("N is a reserved name in Product")
            assert field_name not in ns
            idx = idx_table[field_name]
            ns[field_name] = _make_prop(field_type, idx)

        # this is all really gross but I don't know how to do this cleanly
        # need to build t so I can call super() in new and init
        # need to exec to get proper signatures
        t = TupleKind.__new__(mcs, name, bases, ns, fields=tuple(fields.values()),
                              **kwargs)
        if t._unbound_base_ is None:
            t._unbound_base_ = cls

        # not strictly necessary could iterative over class dict finding
        # TypedProperty to reconstruct _field_table_ but that seems bad
        t._field_table_ = OrderedFrozenDict(fields)
        return t

    def qualify(cls, direction):
        new_fields = OrderedDict()
        base = cls
        for k, v in cls.field_dict.items():
            new_fields[k] = v.qualify(direction)
        for k, v in cls.field_dict.items():
            if not issubclass(new_fields[k], v):
                base = cls.unbound_t
        if base.is_bound and all(v == base.field_dict[k] for k, v in
                                 new_fields.items()):
            return base

        return cls.unbound_t._cache_handler(cls.is_cached, new_fields,
                                            cls.__name__, (base, ), {})

    def flip(cls):
        new_fields = OrderedDict()
        base = cls
        for k, v in cls.field_dict.items():
            new_fields[k] = v.flip()
        for k, v in cls.field_dict.items():
            if not issubclass(new_fields[k], v):
                base = cls.qualify(Direction.Undirected)
        return cls.unbound_t._cache_handler(cls.is_cached, new_fields,
                                            cls.__name__, (base, ), {})

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

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if len(ts) == len(self) and self.iswhole(ts):
            return ts[0].name.tuple

        return namedtuple(**dict(zip(self.keys(),ts)))


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

    if t == Tuple:
        return t[tuple(decl.values())](*args)
    assert t == Product
    return t.from_fields("anon", decl)(*args)


def namedtuple(**kwargs):
    return tuple_(kwargs, t=Product)
