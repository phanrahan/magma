from functools import lru_cache
import functools
import operator
from collections import OrderedDict
from hwtypes.adt import (
    TupleMeta,
    Tuple as Tuple_,
    AnonymousProductMeta,
    ProductMeta,
)
from hwtypes import BitVector, Bit
from hwtypes.adt_meta import BoundMeta, RESERVED_SUNDERS, ReservedNameError
from hwtypes.util import TypedProperty, OrderedFrozenDict
from .common import deprecated
from .ref import TupleRef
from .t import Type, Kind, Direction
from .compatibility import IntegerTypes
from .debug import debug_wire, get_debug_info, debug_unwire
from .logging import root_logger
from .protocol_type import magma_type, magma_value

from magma.wire_container import (WiringLog, AggregateWireable,
                                  aggregate_wireable_method)
from magma.wire import wire
from magma.protocol_type import MagmaProtocol
from magma.operator_utils import output_only


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
                raise ReservedNameError(f'class attribute {rname} is reserved '
                                        'by the type machinery')

        bound_types = fields
        has_bound_base = False
        unbound_bases = []
        for base in bases:
            if isinstance(base, BoundMeta):
                if base.is_bound:
                    has_bound_base = True
                    if bound_types is None:
                        bound_types = base.fields
                    else:
                        for x, y in zip(bound_types, base.fields):
                            if not (issubclass(x, y) or issubclass(y, x)):
                                try:
                                    if x.is_bindable(y):
                                        continue
                                except AttributeError:
                                    pass
                                try:
                                    if y.is_bindable(x):
                                        continue
                                except AttributeError:
                                    pass
                                raise TypeError(
                                    "Can't inherit from multiple different "
                                    "bound_types"
                                )
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
        if any(x is not y for x, y in zip(undirected_idx, idx)):
            bases = [cls[undirected_idx]]
        else:
            bases = [cls]
        bases = tuple(bases)
        class_name = cls._name_cb(idx)

        t = mcs(class_name, bases, {'__module__': cls.__module__}, fields=idx)
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

    @property
    @lru_cache()
    def direction(cls):
        directions = iter(t.direction for t in cls.fields)
        first = next(directions)
        if all(d == first for d in directions):
            return first
        return None

    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args)
        obj.__init__(*args, **kwargs)
        return obj

    @property
    def N(cls):
        return len(cls.fields)

    def __len__(cls):
        return cls.N

    def __str__(cls):
        if not cls.is_bound:
            return cls.__name__
        s = "Tuple("
        s += ",".join(str(T) for T in cls.fields)
        s += ")"
        return s

    def is_wireable(cls, rhs):
        rhs = magma_type(rhs)
        if not isinstance(rhs, TupleKind) or len(cls.fields) != len(rhs.fields):
            return False
        for idx, T in enumerate(cls.fields):
            if not T.is_wireable(rhs[idx]):
                return False
        return True

    def is_bindable(cls, rhs):
        rhs = magma_type(rhs)
        if not isinstance(rhs, TupleKind) or len(cls.fields) != len(rhs.fields):
            return False
        for idx, T in enumerate(cls.fields):
            if not T.is_bindable(rhs[idx]):
                return False
        return True

    def __eq__(cls, rhs):
        if not isinstance(rhs, TupleKind):
            return False

        if not cls.is_bound:
            return not rhs.is_bound

        return cls.fields == rhs.fields

    __hash__ = TupleMeta.__hash__


class Tuple(Type, Tuple_, AggregateWireable, metaclass=TupleKind):
    def __init__(self, *largs, **kwargs):

        Type.__init__(self, **kwargs)
        AggregateWireable.__init__(self)

        self._ts = {}
        if largs:
            assert len(largs) == len(self)
            for i, (k, t, T) in enumerate(zip(self.keys(),
                                              largs,
                                              self.types())):
                if isinstance(t, (IntegerTypes, BitVector, Bit)):
                    t = T(t)
                self._ts[i] = t
                if not isinstance(self, AnonProduct):
                    setattr(self, k, t)
            self._resolved = True

        self._keys_list = list(self.keys())

    def __getattr__(self, key):
        if not isinstance(self, AnonProduct) and key in self.keys():
            # On demand setattr for lazy children
            t = self[key]
            setattr(self, key, t)
            return t
        return object.__getattribute__(self, key)

    __hash__ = Type.__hash__

    @classmethod
    def is_oriented(cls, direction):
        return all(v.is_oriented(direction) for v in cls.fields)

    @classmethod
    def is_clock(cls):
        return False

    @classmethod
    @deprecated
    def isoriented(cls, direction):
        return cls.is_oriented(direction)

    @classmethod
    def keys(cls):
        return [str(i) for i in range(len(cls.fields))]

    @output_only("Cannot use == on an input")
    def __eq__(self, rhs):
        if not isinstance(rhs, type(self)):
            return NotImplemented
        else:
            # NOTE: Use functools.reduce so import * doesn't clobber m.reduce
            # from bits
            return functools.reduce(operator.and_,
                                    (x == y for x, y in zip(self, rhs)))

    @output_only("Cannot use != on an input")
    def __ne__(self, rhs):
        return ~(self == rhs)

    def __repr__(self):
        if not self.name.anon():
            return super().__repr__()
        ts = [repr(t) for t in self]
        kts = ['{}={}'.format(k, v) for k, v in zip(self.keys(), ts)]
        return 'tuple(dict({})'.format(', '.join(kts))

    def _make_t(self, idx):
        T = self.types()[idx]
        ref = TupleRef(self, self._keys_list[idx])
        if issubclass(T, MagmaProtocol):
            value = T._from_magma_ref_(ref)
        else:
            value = T(name=ref)
        value.set_enclosing_when_context(self._enclosing_when_context)
        return value

    def has_elaborated_children(self):
        return bool(self._ts)

    def _enumerate_children(self):
        return self.items()

    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                key = list(self.keys()).index(key)
            except ValueError:
                raise KeyError(key) from None
        if not isinstance(key, int):
            raise KeyError(key)
        if key not in self._ts:
            self._ts[key] = self._make_t(key)
            self._ts[key].parent = self
        return self._ts[key]

    @property
    def ts(self):
        return [self[k] for k in self.keys()]

    def __setitem__(self, key, val):
        old = self[key]
        if old is not val:
            _logger.error(
                WiringLog(f"May not mutate tuple, trying to replace "
                          f"{{}}[{key}] ({{}}) with {{}}", self, old, val)
            )

    def __len__(self):
        return len(type(self).fields)

    @classmethod
    def flat_length(cls):
        return sum(magma_type(T).flat_length() for T in cls.types())

    def __call__(self, o):
        return self.wire(o, get_debug_info(3))

    @debug_wire
    def wire(self, o, debug_info):
        o = magma_value(o)
        if not isinstance(o, Tuple):
            _logger.error(
                WiringLog(f"Cannot wire {{}} (type={type(o)}) to {{}} "
                          f"(type={type(self)}) because {{}} is not a Tuple",
                          o, self, o),
                debug_info=debug_info
            )
            return

        if self.keys() != o.keys():
            _logger.error(
                WiringLog(f"Cannot wire {{}} (type={type(o)}, "
                          f"keys={list(self.keys())}) to "
                          f" {{}} (type={type(self)}, "
                          f"keys={list(o.keys())}) because the tuples do not "
                          f"have the same keys", o, self),
                debug_info=debug_info
            )
            return
        if self._should_wire_children(o):
            for self_elem, o_elem in zip(self, o):
                self_elem = magma_value(self_elem)
                o_elem = magma_value(o_elem)
                wire(o_elem, self_elem, debug_info)
        else:
            AggregateWireable.wire(self, o, debug_info)

    @debug_unwire
    @aggregate_wireable_method
    def unwire(self, o=None, debug_info=None, keep_wired_when_contexts=False):
        for k, t in self.items():
            if o is None:
                t.unwire(debug_info=debug_info,
                         keep_wired_when_contexts=keep_wired_when_contexts)
            elif o[k].is_input():
                o[k].unwire(t, debug_info=debug_info,
                            keep_wired_when_contexts=keep_wired_when_contexts)
            else:
                t.unwire(o[k], debug_info=debug_info,
                         keep_wired_when_contexts=keep_wired_when_contexts)

    @aggregate_wireable_method
    def driven(self):
        return all(t.driven() for t in self)

    @aggregate_wireable_method
    def wired(self):
        return all(t.wired() for t in self)

    @staticmethod
    def _iswhole(ts, keys):

        for i in range(len(ts)):
            if ts[i].anon():
                return False

        for i in range(len(ts)):
            # elements must be an tuple reference
            if not isinstance(ts[i].name, TupleRef):
                return False

        for i in range(1, len(ts)):
            # elements must refer to the same tuple
            if ts[i].name.tuple is not ts[i - 1].name.tuple:
                return False

        for i in range(len(ts)):
            # elements should be numbered consecutively
            if ts[i].name.index != list(keys)[i]:
                return False

        if len(ts) != len(ts[0].name.tuple):
            # elements should refer to a whole tuple
            return False

        return True

    def iswhole(self):
        return Tuple._iswhole(list(self), self.keys())

    @aggregate_wireable_method
    def trace(self, skip_self=True):
        ts = []
        for t in self:
            result = t.trace(skip_self)
            if result is not None:
                ts.append(result)
            elif not skip_self and (t.is_output() or t.is_inout()):
                ts.append(t)
            else:
                return None

        if len(ts) == len(self) and Tuple._iswhole(ts, self.keys()):
            return ts[0].name.tuple

        return type(self).flip()(*ts)

    @aggregate_wireable_method
    def value(self):
        ts = [t.value() for t in self]

        for t in ts:
            if t is None:
                return None

        if len(ts) == len(self) and Tuple._iswhole(ts, self.keys()):
            return ts[0].name.tuple

        return type(self).flip()(*ts)

    @aggregate_wireable_method
    def driving(self):
        return {k: t.driving() for k, t in self.items()}

    @classmethod
    def unflatten(cls, value):
        values = []
        offset = 0
        for field in cls.fields:
            size = field.flat_length()
            ts = value[offset:offset + size]
            values.append(field.unflatten(ts))
            offset += size
        return cls(*values)

    def flatten(self):
        return sum([t.flatten() for t in self], [])

    def const(self):
        return all(t.const() for t in self)

    @classmethod
    def types(cls):
        return cls.fields

    def values(self):
        return list(self)

    def items(self):
        return zip(self.keys(), self)

    def undriven(self):
        for elem in self:
            elem.undriven()

    def unused(self):
        for elem in self:
            elem.unused()

    @classmethod
    def is_mixed(cls):
        input, output, inout, mixed = False, False, False, False
        for field in cls.fields:
            input |= field.is_input()
            output |= field.is_output()
            inout |= field.is_inout()
            mixed |= field.is_mixed()
        return mixed or (input + output + inout) > 1

    def connection_iter(self, only_slice_bits=False):
        for elem in self:
            yield elem, elem.trace()

    def has_children(self):
        return True

    def set_enclosing_when_context(self, ctx):
        self._enclosing_when_context = ctx
        for value in self._ts.values():
            value.set_enclosing_when_context(ctx)


def _add_properties(ns, fields):
    def _make_prop(field_type, idx):
        @TypedProperty(field_type)
        def prop(self):
            return self[idx]

        @prop.setter
        def prop(self, value):
            self[idx] = value

        return prop

    for idx, (field_name, field_type) in enumerate(fields.items()):
        if field_name == "N":
            # TODO: Make N unreserved
            raise ValueError("N is a reserved name in Product")
        assert field_name not in ns
        ns[field_name] = _make_prop(field_type, idx)


class AnonProductKind(AnonymousProductMeta, TupleKind, Kind):
    __hash__ = type.__hash__

    def _from_idx(cls, idx):
        mcs = type(cls)

        try:
            return mcs._class_cache[cls, idx]
        except KeyError:
            pass

        if cls.is_bound:
            raise TypeError('Type is already bound')

        undirected_idx = OrderedFrozenDict(
            [(k, v.qualify(Direction.Undirected)) for k, v in idx.items()]
        )
        if undirected_idx != idx:
            bases = [cls[undirected_idx]]
        else:
            bases = [cls]
        bases = tuple(bases)
        class_name = cls._name_from_idx(idx)

        ns = {'__module__': cls.__module__}
        # add properties to namespace
        # build properties
        _add_properties(ns, idx)

        t = mcs(class_name, bases, ns, fields=tuple(idx.values()))
        t._field_table_ = idx
        if t._unbound_base_ is None:
            t._unbound_base_ = cls
        mcs._class_cache[cls, idx] = t
        t._cached_ = True
        return t

    def qualify(cls, direction):
        new_fields = OrderedDict()
        base = cls
        for k, v in cls.field_dict.items():
            new_fields[k] = v.qualify(direction)
        for k, v in cls.field_dict.items():
            if not issubclass(new_fields[k], v):
                base = cls.unbound_t
        if base.is_bound and all(v is base.field_dict[k]
                                 for k, v in new_fields.items()):
            return base

        if cls.unbound_t is AnonProduct:
            return cls.unbound_t._cache_handler(OrderedFrozenDict(new_fields))
        else:
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
        if cls.unbound_t is AnonProduct:
            return cls.unbound_t._cache_handler(OrderedFrozenDict(new_fields))
        else:
            return cls.unbound_t._cache_handler(cls.is_cached, new_fields,
                                                cls.__name__, (base, ), {})

    def __eq__(cls, rhs):
        if not isinstance(rhs, AnonProductKind):
            return False

        if not cls.is_bound:
            return not rhs.is_bound

        return cls.field_dict == rhs.field_dict

    def is_wireable(cls, rhs):
        rhs = magma_type(rhs)
        if (
            not isinstance(rhs, AnonProductKind) or
            len(cls.fields) != len(rhs.fields)
        ):
            return False
        for k, v in cls.field_dict.items():
            if k not in rhs.field_dict or not v.is_wireable(rhs.field_dict[k]):
                return False
        return True

    def is_bindable(cls, rhs):
        rhs = magma_type(rhs)
        if (
            not isinstance(rhs, AnonProductKind) or
            len(cls.fields) != len(rhs.fields)
        ):
            return False
        for k, v in cls.field_dict.items():
            if k not in rhs.field_dict or not v.is_bindable(rhs.field_dict[k]):
                return False
        return True

    def __len__(cls):
        return len(cls.fields)

    def __str__(cls):
        if not cls.is_bound:
            return cls.__name__
        s = "Tuple("
        s += ",".join(f'{k}={str(v)}' for k, v in cls.field_dict.items())
        s += ")"
        return s


class AnonProduct(Tuple, metaclass=AnonProductKind):
    @classmethod
    def keys(cls):
        return cls.field_dict.keys()


class ProductKind(ProductMeta, AnonProductKind, Kind):
    __hash__ = type.__hash__

    def __new__(mcs, name, bases, namespace, cache=True, **kwargs):
        return super().__new__(mcs, name, bases, namespace, cache, **kwargs)

    def from_fields(cls, name, fields, cache=True):
        return super().from_fields(name, fields, cache)

    @classmethod
    def _from_fields(mcs, fields, name, bases, ns, **kwargs):

        cls = bases[0]

        # add properties to namespace
        # build properties
        _add_properties(ns, fields)

        # this is all really gross but I don't know how to do this cleanly
        # need to build t so I can call super() in new and init
        # need to exec to get proper signatures
        t = TupleKind.__new__(mcs, name, bases, ns,
                              fields=tuple(fields.values()), **kwargs)
        if t._unbound_base_ is None:
            t._unbound_base_ = cls

        # not strictly necessary could iterative over class dict finding
        # TypedProperty to reconstruct _field_table_ but that seems bad
        t._field_table_ = OrderedFrozenDict(fields)
        return t


class Product(AnonProduct, metaclass=ProductKind):
    pass
