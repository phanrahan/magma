import weakref
from functools import reduce
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
from magma.wire_container import WiringLog
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
        if (N ,T) == (None, None):
            #class is abstract so t.abstract -> t
            type_._info_ = type_, N, T
        elif info[0] is None:
            #class inherited from concrete type so there is no abstract t
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
                if len(index[0]) == 0 :
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
        bases.extend(b[index] for b in cls.__bases__ if isinstance(b, mcs))
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
        type_ = mcs(class_name, bases, {"orig_name": orig_name}, info=(cls, ) + index)
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
        return f"Array[{cls.N}, {cls.T}]"

    def __repr__(cls):
        return f"Array[{cls.N}, {cls.T}]"

    def qualify(cls, direction):
        # Handle qualified, unsized/child e.g. In(Array) and In(Out(Array))
        if cls.T is None or isinstance(cls.T, Direction):
            return cls[None, direction]
        return cls[cls.N, cls.T.qualify(direction)]

    def flip(cls):
        return cls[cls.N, cls.T.flip()]

    def __eq__(cls, rhs):
        if not isinstance(rhs, ArrayMeta):
            return NotImplemented
        return (cls.N == rhs.N) and (cls.T == rhs.T)

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


class Array(Type, metaclass=ArrayMeta):
    def __init__(self, *args, **kwargs):
        Type.__init__(self, **kwargs)
        self.ts = []
        if args:
            if len(args) == 1 and isinstance(args[0], (list, Array, int,
                                                       BitVector)):
                if isinstance(args[0], list):
                    if len(args[0]) != self.N:
                        raise ValueError("Array list constructor can only be used "
                                         "with list equal to array length")
                    self.ts = []
                    for elem in args[0]:
                        if isinstance(elem, int):
                            self.ts.append(self.T(elem))
                        else:
                            self.ts.append(elem)
                elif isinstance(args[0], Array):
                    if len(args[0]) != len(self):
                        raise TypeError(f"Will not do implicit conversion of arrays")
                    self.ts = args[0].ts[:]
                elif isinstance(args[0], (BitVector, int)):
                    if not issubclass(self.T, Bit):
                        raise TypeError(f"Can only instantiate Array[N, Bit] "
                                        f"with int/bv, not Array[N, {self.T}]")
                    if (isinstance(args[0], BitVector) and
                            len(args[0]) != self.N):
                        raise TypeError(
                            f"Cannot create a value of type {type(self)} with"
                            f" a BitVector of length {len(args[0])} (the sizes"
                            " must match)"
                        )

                    n = args[0]
                    bits = (int2seq(n, self.N)
                            if isinstance(n, int)
                            else n.bits())
                    self.ts = []
                    for bit in bits:
                        self.ts.append(self.T(bit))
                elif self.N == 1:
                    t = args[0]
                    if isinstance(t, IntegerTypes):
                        t = self.T(t)
                    assert type(t) == self.T or type(t) == self.T.flip() or \
                        issubclass(type(type(t)), type(self.T)) or \
                        issubclass(type(self.T), type(type(t))), (type(t), self.T)
                    self.ts = [t]
            elif len(args) == self.N:
                self.ts = []
                for t in args:
                    if isinstance(t, IntegerTypes):
                        t = self.T(t)
                    assert type(t) == self.T or type(t) == self.T.flip() or \
                        issubclass(type(type(t)), type(self.T)) or \
                        issubclass(type(self.T), type(type(t))), (type(t), self.T)
                    self.ts.append(t)
            else:
                raise TypeError(f"Constructing array with {args} not supported")
        else:
            for i in range(self.N):
                T = self.T
                ref = ArrayRef(self, i)
                if issubclass(T, MagmaProtocol):
                    t = T._from_magma_value_(T._to_magma_()(name=ref))
                else:
                    t = T(name=ref)
                self.ts.append(t)

    @classmethod
    def is_oriented(cls, direction):
        if cls.T is None:
            return False
        return cls.T.is_oriented(direction)

    @classmethod
    def is_clock(cls):
        return False

    @classmethod
    @deprecated
    def isoriented(cls, direction):
        return cls.is_oriented(direction)

    @output_only("Cannot use == on an input")
    def __eq__(self, rhs):
        if not isinstance(rhs, ArrayType):
            return False
        return self.ts == rhs.ts

    @output_only("Cannot use != on an input")
    def __ne__(self, rhs):
        return ~(self == rhs)

    __hash__ = Type.__hash__

    def __repr__(self):
        if self.name.anon():
            t_strs = ', '.join(repr(t) for t in self.ts)
            return f'array([{t_strs}])'
        return super().__repr__()

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

    def __getitem__(self, key):
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
        if isinstance(key, Type):
            # indexed using a dynamic magma value, generate mux circuit
            return self.dynamic_mux_select(key)
        if isinstance(key, slice):
            if not _is_valid_slice(self.N, key):
                raise IndexError(f"array index out of range "
                                 f"(type={type(self)}, key={key})")
            _slice = [self[i] for i in range(*key.indices(len(self)))]
            return type(self)[len(_slice), self.T](_slice)
        else:
            if isinstance(key, BitVector):
                key = key.as_uint()

            if not (-self.N <= key and key < self.N):
                raise IndexError(f"{key}, {self.N}")

            return self.ts[key]

    def __setitem__(self, key, val):
        error = False
        old = self[key]
        if isinstance(old, Array):
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
        elif old is not val:
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

    @classmethod
    def is_oriented(cls, direction):
        return cls.T.is_oriented(direction)

    def as_list(self):
        return [self[i] for i in range(len(self))]

    @debug_wire
    def wire(i, o, debug_info):
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

        for k in range(len(i)):
            i[k].wire(o[k], debug_info)

    def unwire(i, o):
        for k in range(len(i)):
            i[k].unwire(o[k])

    def driven(self):
        for t in self.ts:
            if not t.driven():
                return False
        return True

    def driving(self):
        return [t.driving() for t in self]

    def wired(self):
        for t in self.ts:
            if not t.wired():
                return False
        return True

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

    def iswhole(self):
        return Array._iswhole(self.ts)

    def trace(self):
        ts = [t.trace() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if Array._iswhole(ts):
            return ts[0].name.array

        return type(self).flip()(ts)

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if Array._iswhole(ts):
            return ts[0].name.array

        return type(self).flip()(ts)

    def const(self):
        for t in self.ts:
            if not t.const():
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

    def flatten(self):
        return sum([t.flatten() for t in self.ts], [])

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


ArrayType = Array
