import weakref
from functools import reduce, lru_cache
from abc import ABCMeta
from hwtypes import BitVector
from .common import deprecated
from .ref import AnonRef, ArrayRef
from .t import Type, Kind, Direction, In, Out
from .compatibility import IntegerTypes
from .digital import Digital
from .bit import Bit
from .bitutils import int2seq, seq2int
from .debug import debug_wire, get_callee_frame_info
from .logging import root_logger
from .protocol_type import magma_type, magma_value

from magma.operator_utils import output_only
from magma.wire_container import WiringLog, Wire, Wireable
from magma.protocol_type import MagmaProtocol


_logger = root_logger()


class ArrayMeta(ABCMeta, Kind):
    # BitVectorType, size :  BitVectorType[size]
    _class_cache = weakref.WeakValueDictionary()

    def __new__(cls, name, bases, namespace, info=(None, None, None), **kwargs):
        # TODO: A lot of this code is shared with AbstractBitVectorMeta, we
        # should refactor to reuse
        if '_info_' in namespace:
            raise TypeError(
                'class attribute _info_ is reversed by the type machinery')

        N, T = info[1:3]
        for base in bases:
            if getattr(base, 'is_concrete', False):
                if (N, T) == (None, None):
                    (N, T) = (base.N, base.T)
                elif N != base.N:
                    raise TypeError(
                        "Can't inherit from multiple arrays with different N")
                elif not issubclass(T, base.T):
                    raise TypeError(
                        "Can't inherit from multiple arrays with different T")

        namespace['_info_'] = info[0], N, T
        type_ = super().__new__(cls, name, bases, namespace, **kwargs)
        if (N, T) == (None, None):
            # class is abstract so t.abstract -> t
            type_._info_ = type_, N, T
        elif info[0] is None:
            # class inherited from concrete type so there is no abstract t
            type_._info_ = None, N, T

        return type_

    def __getitem__(cls, index: tuple) -> 'ArrayMeta':
        mcs = type(cls)

        # If cls.T is a direction, and the new T (index[1])
        if isinstance(cls.T, Direction):
            # If we're replacing a direction (e.g. `In(Out(Array)))`, just use
            # the default direction logic
            if not isinstance(index[1], Direction):
                # Otherwise, we expect that we're qualifying a Type with the
                # direction (e.g. In(Array)[5, Bit])
                if not issubclass(index[1], Type):
                    raise TypeError("Expected Type as second index to Array")
                if not index[1].is_oriented(cls.T):
                    _logger.warning(
                        f"Parametrizing qualifed Array {cls} with inner type "
                        f" {index[1]} which doesn't match, will use array "
                        "qualifier"
                    )
                index = index[0], index[1].qualify(cls.T)
        elif cls.T is None:
            # Else, it index[1] should be  Type (e.g. In(Bit)) or a Direction
            # (used internally for In(Array))
            valid_second_index = (isinstance(index[1], Direction) or
                                  issubclass(magma_type(index[1]), Type))
            if not valid_second_index:
                raise TypeError(
                    "Expected Type or Direction as second index to Array"
                    f" got: {index[1], type(index[1])}"
                )

        try:
            return mcs._class_cache[cls, index]
        except KeyError:
            pass

        if not (isinstance(index, tuple) and len(index) == 2):
            raise TypeError('Parameters to array must be a tuple of length 2')

        # index[0] (N) can be None (used internally for In(Array))
        if index[0] is not None:
            if isinstance(index[0], tuple):
                if len(index[0]) == 0:
                    raise ValueError("Cannot create array with length 0 tuple "
                                     "for N")
                if len(index[0]) > 1:
                    T = index[1]
                    # ND Array
                    for N in index[0]:
                        T = Array[N, T]
                    return T
                # len(index[0]) == 1, Treat as normal Array
                index = index[0]

            if (not isinstance(index[0], int) or index[0] <= 0):
                raise TypeError(
                    'Length of array must be an int greater than 0, got:'
                    f' {index[0]}'
                )

        if cls.is_concrete:
            if index[0] == cls.N and index[1] is cls.T:
                return cls
            else:
                return cls.abstract_t[index]

        bases = []
        bases.extend(b[index] for b in cls.__bases__
                     if isinstance(b, mcs))
        # only add base classes if we're have a child type
        # (skipped in the case of In(Array))
        if not isinstance(index[1], Direction):
            bases.extend(cls[index[0], b] for b in index[1].__bases__ if
                         isinstance(b, type(magma_type(index[1]))))
        if not any(issubclass(b, cls) for b in bases):
            bases.insert(0, cls)
        bases = tuple(bases)
        orig_name = cls.__name__
        if isinstance(index[1], Direction):
            class_name = f'{index[1].name}({cls.__name__})'
        else:
            class_name = '{}[{}]'.format(cls.__name__, index)
        type_ = mcs(class_name, bases, {"orig_name": orig_name},
                    info=(cls, ) + index)
        type_.__module__ = cls.__module__
        mcs._class_cache[cls, index] = type_
        return type_

    @property
    def abstract_t(cls) -> 'ArrayMeta':
        t = cls._info_[0]
        if t is not None:
            return t
        else:
            raise AttributeError('type {} has no abstract_t'.format(cls))

    @property
    def undirected_t(cls) -> 'ArrayMeta':
        T = cls.T
        if cls.is_concrete:
            return cls[cls.N, cls.T.qualify(Direction.Undirected)]
        else:
            raise AttributeError('type {} has no undirected_t'.format(cls))

    @property
    def N(cls) -> int:
        return cls._info_[1]

    @property
    def T(cls):
        return cls._info_[2]

    @property
    def is_concrete(cls) -> bool:
        return (cls.N, cls.T) != (None, None)

    def __len__(cls):
        return cls.N

    def __str__(cls):
        # handle In(Array)
        if isinstance(cls.T, Direction):
            assert cls.N is None
            return f"{cls.T.name}(Array)"
        return cls.__name__

    def __repr__(cls):
        return f"{cls.__name__}"

    @lru_cache()
    def qualify(cls, direction):
        # Handle qualified, unsized/child e.g. In(Array) and In(Out(Array))
        if cls.T is None or isinstance(cls.T, Direction):
            return cls[None, direction]
        if cls.direction == direction:
            return cls
        return cls[cls.N, cls.T.qualify(direction)]

    @lru_cache()
    def flip(cls):
        return cls[cls.N, cls.T.flip()]

    @property
    @lru_cache()
    def direction(cls):
        return cls.T.direction

    def __eq__(cls, rhs):
        if not isinstance(rhs, ArrayMeta):
            return NotImplemented
        return (cls.N == rhs.N) and (cls.T == rhs.T)

    @lru_cache()
    def is_wireable(cls, rhs):
        rhs = magma_type(rhs)
        if not isinstance(rhs, ArrayMeta) or cls.N != rhs.N:
            return False
        return cls.T.is_wireable(rhs.T)

    def is_bindable(cls, rhs):
        rhs = magma_type(rhs)
        if not isinstance(rhs, ArrayMeta) or cls.N != rhs.N:
            return False
        return cls.T.is_bindable(rhs.T)

    __hash__ = type.__hash__


def _is_valid_slice(N, key):
    start, stop = key.start, key.stop
    return (((start is None or (start < N and start >= -N))) and
            (stop is None or (stop <= N and stop > -N)))


def _make_array_from_list(N, T, arg):
    if len(arg) != N:
        raise ValueError("Array list constructor can only be used "
                         "with list equal to array length")
    return [elem if not isinstance(elem, int) else T(elem)
            for elem in arg]


def _make_array_from_array(N, arg):
    if len(arg) != N:
        raise TypeError(f"Will not do implicit conversion of arrays")
    return arg.ts[:]


def _make_array_from_bv(N, T, arg):
    if not issubclass(T, Bit):
        raise TypeError(f"Can only instantiate Array[N, Bit] "
                        f"with int/bv, not Array[N, {T}]")
    if isinstance(arg, BitVector) and len(arg) != N:
        raise TypeError(
            f"Cannot construct Array[{N}, {T}] with BitVector of length "
            f"{len(arg)} (sizes must match)")
    if isinstance(arg, int) and arg.bit_length() > N:
        raise ValueError(
            f"Cannot construct Array[{N}, {T}] with integer {arg} "
            f"(requires truncation)")
    bits = int2seq(arg, N) if isinstance(arg, int) else arg.bits()
    return [T(bit) for bit in bits]


def _check_arg(N, T, arg):
    assert (type(arg) == T or type(arg) == T.flip() or
            issubclass(type(type(arg)), type(T)) or
            issubclass(type(T), type(type(arg)))), (type(arg), T)


def _make_array_length_one(T, arg):
    if isinstance(arg, IntegerTypes):
        arg = T(arg)
    return [arg]


def _make_array_length_n(N, T, args):
    ts = [T(t) if isinstance(t, IntegerTypes) else t for t in args]
    for t in ts:
        _check_arg(N, T, t)
    return ts


def _make_array_no_args(array):
    T = array.T
    refs = [ArrayRef(array, i) for i in range(array.N)]
    if not issubclass(T, MagmaProtocol):
        return [T(name=ref) for ref in refs]
    return [T._from_magma_value_(T._to_magma_()(name=ref)) for ref in refs]


def _make_array_from_args(N, T, args):
    if len(args) == 1 and isinstance(args[0], (list, Array, int, BitVector)):
        if isinstance(args[0], list):
            return _make_array_from_list(N, T, args[0])
        if isinstance(args[0], Array):
            return _make_array_from_array(N, args[0])
        if isinstance(args[0], (BitVector, int)):
            return _make_array_from_bv(N, T, args[0])
        if N == 1:
            return _make_array_length_one(T, args[0])
    if len(args) == N:
        return _make_array_length_n(N, T, args)
    raise TypeError(f"Constructing array with {args} not supported")


def _make_array(array, args):
    if args:
        return _make_array_from_args(array.N, array.T, args)
    return _make_array_no_args(array)


def _is_slice_child(child):
    return isinstance(child, Array) and child._is_slice()


class Array(Type, Wireable, metaclass=ArrayMeta):
    def __init__(self, *args, **kwargs):
        Type.__init__(self, **kwargs)
        Wireable.__init__(self)
        self._ts = {}
        self._slices = {}
        self._slices_by_start_index = {}
        if args:
            for i, t in enumerate(_make_array(self, args)):
                self._ts[i] = t

    @classmethod
    def is_oriented(cls, direction):
        if cls.T is None:
            return False
        return cls.T.is_oriented(direction)

    @classmethod
    def is_clock(cls):
        return False

    @output_only("Cannot use == on an input")
    def __eq__(self, rhs):
        if not isinstance(rhs, ArrayType):
            return False
        return self.ts == rhs.ts

    @output_only("Cannot use != on an input")
    def __ne__(self, rhs):
        return ~(self == rhs)

    __hash__ = Type.__hash__

    @property
    def T(self):
        return type(self).T

    @property
    def N(self):
        return type(self).N

    def __len__(self):
        return self.N

    @classmethod
    def flat_length(cls):
        return cls.N * cls.T.flat_length()

    def _is_whole_slice(self, key):
        # check if it's any of `x[:], x[0:], x[:len(x)], x[0:len(x)]`
        return (isinstance(key[-1], slice) and
                (key[-1] == slice(None) or
                 key[-1] == slice(0, None) or
                 key[-1] == slice(None, len(self)) or
                 key[-1] == slice(0, len(self))))

    def __setitem__(self, key, val):
        old = self[key]
        error = False
        if old is val:
            # Early "exit" (avoid recursion in other branches)
            pass
        elif isinstance(old, Array):
            if len(old) != len(val):
                error = True
            elif issubclass(old.T, Array):
                # If array of array, check that we can do elementwise setitem
                # (will return true if there's an error)
                # We can't just do an `is` check on the children since those
                # might be slices that return new anon values (so x[1:2] is not
                # x[1:2], but their recursive leaf contents should be the same)
                error = any(old.__setitem__(i, val[i])
                            for i in range(len(old)))
            elif any(old[i] is not val[i] for i in range(len(old))):
                error = True
        else:
            error = True

        if error:
            _logger.error(
                WiringLog(f"May not mutate array, trying to replace "
                          f"{{}}[{key}] ({{}}) with {{}}", self, old, val)
            )
        return error

    def __add__(self, other):
        other_len = other.N
        total = self.N + other_len
        res_bits = []
        for i in range(total):
            res_bits.append(self[i] if i < self.N else other[i - self.N])
        return type(self)[len(res_bits), self.T](res_bits)

    def __call__(self, o):
        return self.wire(o, get_callee_frame_info())

    def as_list(self):
        return [self[i] for i in range(len(self))]

    def _check_wireable(self, o, debug_info):
        i = self
        if not isinstance(o, ArrayType):
            if isinstance(o, IntegerTypes):
                _logger.error(
                    WiringLog(f"Cannot wire {o} (type={type(o)}) to {{}} "
                              f"(type={type(i)}) because conversions from "
                              f"IntegerTypes are only defined for Bits, not "
                              f"general Arrays", i),
                    debug_info=debug_info
                )
            else:
                o_str = getattr(o, "debug_name", str(o))
                _logger.error(
                    WiringLog(f"Cannot wire {{}} (type={type(o)}) to {{}} "
                              f"(type={type(i)}) because {{}} is not an Array",
                              o, i, o),
                    debug_info=debug_info
                )
            return

        if i.N != o.N:
            _logger.error(
                WiringLog(f"Cannot wire {{}} (type={type(o)}) to {{}} "
                          f"(type={type(i)}) because the arrays do not have "
                          f"the same length", o, i),
                debug_info=debug_info
            )
            return

    def driving(self):
        if self._ts:
            return [t.driving() for t in self]
        return Wireable.driving(self)

    def wired(self):
        if self._ts:
            for t in self.ts:
                if not t.wired():
                    return False
        return Wireable.wired(self)

    # test whether the values refer a whole array
    @staticmethod
    def _iswhole(ts):

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
            if ts[i].name.array is not ts[i - 1].name.array:
                return False

        if n > 0 and n != ts[0].name.array.N:
            # must use all of the elements of the base array
            return False

        for i in range(n):
            # elements should be numbered consecutively
            if ts[i].name.index != i:
                return False

        return True

    @classmethod
    def unflatten(cls, value):
        size_T = cls.T.flat_length()
        if len(value) != size_T * cls.N:
            raise TypeError("Width mismatch")
        ts = [cls.T.unflatten(value[i:i + size_T])
              for i in range(0, size_T * cls.N, size_T)]
        return cls(ts)

    def concat(self, other) -> 'AbstractBitVector':
        return type(self)[len(self) + len(other), self.T](self.ts + other.ts)

    def undriven(self):
        for elem in self:
            elem.undriven()

    def unused(self):
        for elem in self:
            elem.unused()

    @classmethod
    def is_mixed(cls):
        return cls.T.is_mixed()

    @debug_wire
    def wire(self, o, debug_info):
        o = magma_value(o)
        self._check_wireable(o, debug_info)
        Wireable.wire(self, o, debug_info)
        if self._ts:
            # TODO(leonardt/array2): Optimize performance of this logic, needed
            # for converting Bit to Bits[1] and maintaining value mapping,
            # perhaps we need a variant of Array2 that handles construction
            # with existing values
            for i in range(len(self)):
                if self._get_t(i).value() is not o[i]:
                    self._get_t(i).wire(o[i])

    def unwire(self, o):
        if self._ts:
            for k in range(len(self)):
                self[k].unwire(o[k])
            assert not Wireable.wired(self)
        else:
            Wireable.unwire(self, o)

    def iswhole(self):
        if self._has_children():
            return Array._iswhole(self._collect_children(lambda x: x))
        return True

    def const(self):
        if self._ts:
            return all(t.const() for t in self)
        return False

    def _resolve_bulk_wire(self):
        """
        If a child reference is made, we "expand" a bulk wire into the
        constiuent children to maintain consistency
        """
        if self._wire.driven():
            value = self._wire.value()
            Wireable.unwire(self, value)
            for i in range(len(self)):
                self._get_t(i).wire(value[i])

    def _make_t(self, index):
        if issubclass(self.T, MagmaProtocol):
            return self.T._from_magma_value_(
                self.T._to_magma_()(name=ArrayRef(self, index)))
        else:
            return self.T(name=ArrayRef(self, index))

    def _get_t(self, index):
        if index not in self._ts:
            if self._is_slice():
                # Maintain consistency by always fetching child object from top
                # level array
                return self.name.array._get_t(self.name.index.start + index)
            self._ts[index] = t = self._make_t(index)
            # Update existing slices to have matching child references
            for k, v in list(self._slices.items()):
                if k[0] <= index < k[1]:
                    assert v._ts.get(index - k[0], t) is t
                    v._ts[index - k[0]] = t
                    # TODO(leonardt/array2): Can we compute the range of get_t
                    # needed to avoided extra calls? At least this will just be
                    # a dict lookup so not too expensive
                    for i in range(k[0], k[1]):
                        if i == index:
                            continue
                        self._get_t(i)
                    # Resolve driver
                    # TODO(leonardt/array2): I think we should only ever have 2
                    # overlapping slices (the case when we create a new slice
                    # and call _get_t to resolve them).  We should (a) validate
                    # this assumption, and (b) optimize for this case (can we
                    # exit early once we encounter the slices of interest?)
                    if v._wire.driven():
                        value = v._wire.value()
                        Wireable.unwire(v, value)
                        for i in range(k[0], k[1]):
                            self._ts[i] @= value[i - k[0]]
        self._resolve_bulk_wire()
        return self._ts[index]

    def _resolve_overlapping_indices(self, slice_, value):
        """
        If there's any overlapping children or slices, collect the total range
        of the children and realize them so slices are "expanded" and maintain
        consistency
        """
        overlapping = any(i in self._ts
                          for i in range(slice_.start, slice_.stop))
        start = slice_.start
        stop = slice_.stop
        for k, v in list(self._slices.items()):
            if k == (slice_.start, slice_.stop):
                continue
            if k[0] <= slice_.start < k[1] or k[0] <= slice_.stop < k[1]:
                overlapping = True
        if overlapping:
            for i in range(start, stop):
                # _get_t to populate slice children and resolve any overlaps
                value._ts[i - start] = self._get_t(i)
        return overlapping

    def _get_slice(self, slice_):
        key = (slice_.start, slice_.stop)
        if key not in self._slices:
            # TODO(leonardt/array2): Avoid duplicate logic with expanding for
            # existing chilren
            self._slices[key] = type(self)[slice_.stop - slice_.start, self.T](
                name=ArrayRef(self, slice_)
            )
            self._slices_by_start_index[key[0]] = self._slices[key]
            self._resolve_overlapping_indices(slice_, self._slices[key])
        self._resolve_bulk_wire()
        return self._slices[key]

    def _normalize_slice_key(self, key):
        # Normalize slice by mapping None to concrete int values
        start = key.start if key.start is not None else 0
        if start < 0:
            start = self.N + start
            if start < 0:
                raise IndexError(key)
        stop = key.stop if key.stop is not None else len(self)
        if stop < 0:
            stop = self.N + stop
            if stop < 0:
                raise IndexError(key)
        if key.step is not None:
            raise NotImplementedError("Variable slice step not implemented")
        return slice(start, stop, key.step)

    def __getitem__(self, key):
        if isinstance(key, Type):
            # indexed using a dynamic magma value, generate mux circuit
            return self.dynamic_mux_select(key)
        if isinstance(key, tuple):
            # ND Array key
            if len(key) == 1:
                return self[key[0]]

            if not isinstance(key[-1], slice):
                return self[key[-1]][key[:-1]]
            if not self._is_whole_slice(key):
                # If it's not a slice of the whole array, first slice the
                # current array (self), then replace with a slice of the whole
                # array (this is how we determine that we're ready to traverse
                # into the children)
                this_key = key[-1]
                result = self[this_key][key[:-1] + (slice(None), )]
                return result
            # Last index is selecting the whole array, recurse into the
            # children and slice off the inner indices
            inner_ts = [t[key[:-1]] for t in self.ts]
            # Get the type from the children and return the final value
            return type(self)[len(self), type(inner_ts[0])](inner_ts)
        if isinstance(key, int) and key > self.N - 1:
            raise IndexError()
        if isinstance(key, slice):
            if key.step is not None:
                # Use Python indexing logic
                indices = [i for i in range(len(self))][key]
                return type(self)[len(indices), self.T](
                    [self[i] for i in indices])
            if not _is_valid_slice(self.N, key):
                raise IndexError(f"array index out of range "
                                 f"(type={type(self)}, key={key})")
            key = self._normalize_slice_key(key)
        # For nested references of slice objects, we compute the offset
        # from the original array to simplify bookkeeping as well as
        # reducing the size of the select in the backend
        arr = self
        offset = 0
        if arr._is_slice():
            offset = arr.name.index.start
            arr = arr.name.array

        if isinstance(key, BitVector):
            key = int(key)
        if isinstance(key, int):
            if key < 0:
                key += len(self)
            return arr._get_t(offset + key)
        if isinstance(key, slice):
            return arr._get_slice(slice(offset + key.start,
                                        offset + key.stop))
        raise NotImplementedError(key, type(key))

    def flatten(self):
        # TODO(leonardt/array2): Audit where this is used and optimize to avoid
        # where possible
        ts = []
        for child in self._children_iter():
            ts.extend(child.flatten())
        return ts

    def __repr__(self):
        if self.name.anon():
            t_strs = ', '.join(repr(t) for t in self.ts)
            return f'array([{t_strs}])'
        return Type.__repr__(self)

    @property
    def ts(self):
        return [elem for elem in self]

    def _collect_children(self, func):
        ts = []
        for child in self._children_iter():
            result = func(child)
            if result is None:
                return None
            if _is_slice_child(child) and child.name.array is self:
                # TODO: Could we avoid calling .ts here?
                ts.extend(result.ts)
            else:
                ts.append(result)
        if Array._iswhole(ts):
            return ts[0].name.array
        if all(t.const() for t in ts):
            # Pack into Bits const if possible
            return type(self).flip()(ts)
        return Array[self.N, self.T.flip()](ts)

    def _has_children(self):
        return bool(self._ts) or bool(self._slices)

    def value(self):
        if self._has_children():
            return self._collect_children(lambda x: x.value())
        return super().value()

    def trace(self, skip_self=True):
        if self._has_children():
            def _trace(t):
                result = t.trace(skip_self)
                if result is not None:
                    return result
                if not skip_self and (t.is_output() or t.is_inout()):
                    return t
                return None
            result = self._collect_children(_trace)
            return result
        return super().trace()

    def driven(self):
        if self._has_children():
            for child in self._children_iter():
                if child is None:
                    return False
                if not child.driven():
                    return False
            return True
        return super().driven()

    def _is_slice(self):
        return (isinstance(self.name, ArrayRef) and
                isinstance(self.name.index, slice))

    def _children_iter(self):
        i = 0
        while i < self.N:
            if i in self._ts:
                yield self._ts[i]
                i += 1
            elif i in self._slices_by_start_index:
                # We only need to lookup one slice by start index because if
                # multiple slices overlap, they're children will be realized
                # and in self._ts
                value = self._slices_by_start_index[i]
                slice_ = value.name.index
                # Make sure there's no overlapping children realized (otherwise
                # all this slice children should have been realized)
                for j in range(slice_.start, slice_.stop):
                    assert j not in self._ts
                yield value
                i = slice_.stop
            else:
                yield self[i]
                i += 1

    def connection_iter(self, only_slice_bits=False):
        if self._wire.driven():
            driver = self.trace()
            if driver is None:
                return
            # Anon whole driver, e.g. Bit to Bits[1]
            yield from zip(self, driver)
            return
        for child in self._children_iter():
            if (_is_slice_child(child) and only_slice_bits and
                    not issubclass(self.T, Bit)):
                yield from zip(child, child.trace())
            else:
                yield child, child.trace()

    def has_children(self):
        return True


ArrayType = Array
