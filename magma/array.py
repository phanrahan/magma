import weakref
from functools import reduce
from abc import ABCMeta
import magma as m
from .common import deprecated
from .ref import AnonRef, ArrayRef
from .t import Type, Kind, Direction
from .compatibility import IntegerTypes
from .digital import Digital
from .bit import VCC, GND, Bit
from .bitutils import seq2int
from .debug import debug_wire, get_callee_frame_info
from .logging import root_logger


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
                if (N, T) is (None, None):
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
                                  issubclass(index[1], Type))
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
            if (not isinstance(index[0], int) or index[0] <= 0):
                raise TypeError(
                    'Length of array must be an int greater than 0, got:'
                    f' {index[0]}'
                )


        if cls.is_concrete:
            if index == (cls.N, cls.T):
                return cls
            else:
                return cls.abstract_t[index]

        bases = []
        bases.extend(b[index] for b in cls.__bases__ if isinstance(b, mcs))
        # only add base classes if we're have a child type
        # (skipped in the case of In(Array))
        if not isinstance(index[1], Direction):
            bases.extend(cls[index[0], b] for b in index[1].__bases__ if
                         isinstance(b, type(index[1])))
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

    __hash__ = type.__hash__


class Array(Type, metaclass=ArrayMeta):
    def __init__(self, *args, **kwargs):
        Type.__init__(self, **kwargs)
        self.ts = []
        if args:
            if len(args) == 1 and isinstance(args[0], (list, Array, int)):
                if isinstance(args[0], list):
                    if len(args[0]) != self.N:
                        raise ValueError("Array list constructor can only be used with list equal to array length")
                    self.ts = []
                    for elem in args[0]:
                        if isinstance(elem, int):
                            self.ts.append(VCC if elem else GND)
                        else:
                            self.ts.append(elem)
                elif len(self) > 1 and isinstance(args[0], Array):
                    if len(args[0]) != len(self):
                        raise TypeError(f"Will not do implicit conversion of arrays")
                    self.ts = args[0].ts[:]
                elif isinstance(args[0], int):
                    if not issubclass(self.T, Bit):
                        raise TypeError(f"Can only instantiate Array[N, Bit] "
                                        "with int, not Array[N, {self.T}]")
                    self.ts = []
                    for bit in m.bitutils.int2seq(args[0], self.N):
                        self.ts.append(VCC if bit else GND)
                elif self.N == 1:
                    t = args[0]
                    if isinstance(t, IntegerTypes):
                        t = m.VCC if t else m.GND
                    assert type(t) == self.T or type(t) == self.T.flip() or \
                        issubclass(type(type(t)), type(self.T)) or \
                        issubclass(type(self.T), type(type(t))), (type(t), self.T)
                    self.ts = [t]
            elif len(args) == self.N:
                self.ts = []
                for t in args:
                    if isinstance(t, IntegerTypes):
                        t = VCC if t else GND
                    assert type(t) == self.T or type(t) == self.T.flip() or \
                        issubclass(type(type(t)), type(self.T)) or \
                        issubclass(type(self.T), type(type(t))), (type(t), self.T)
                    self.ts.append(t)
            else:
                raise NotImplementedError(args)
        else:
            for i in range(self.N):
                T = self.T
                t = T(name=ArrayRef(self, i))
                self.ts.append(t)

    @classmethod
    def is_oriented(cls, direction):
        if cls.T is None:
            return False
        return cls.T.is_oriented(direction)

    @classmethod
    @deprecated
    def isoriented(cls, direction):
        return cls.is_oriented(direction)

    def __eq__(self, rhs):
        if not isinstance(rhs, ArrayType):
            return False
        return self.ts == rhs.ts

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

    def dynamic_mux_select(self, key):
        return m.operators.Mux(len(self), self.T)(*self.ts, key)

    def __getitem__(self, key):
        if isinstance(key, Type):
            # indexed using a dynamic magma value, generate mux circuit
            return self.dynamic_mux_select(key)
        if isinstance(key, ArrayType) and all(t in {VCC, GND} for t in key.ts):
            key = seq2int([0 if t is GND else 1 for t in key.ts])
        if isinstance(key, slice):
            _slice = [self[i] for i in range(*key.indices(len(self)))]
            return type(self)[len(_slice), self.T](_slice)
        else:
            if not (-self.N <= key and key < self.N):
                raise IndexError

            return self.ts[key]

    def __setitem__(self, key, val):
        error = False
        old = self[key]
        if isinstance(old, Array):
            if len(old) != len(val):
                error = True
            elif any(old[i] is not val[i] for i in range(len(old))):
                error = True
        elif old is not val:
            error = True

        if error:
            _logger.error(f'May not mutate array, trying to replace '
                          f'{self}[{key}] ({old}) with {val}')


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
        # print('Array.wire(', o, ', ', i, ')')

        if not isinstance(o, ArrayType):
            if isinstance(o, IntegerTypes):
                _logger.error(f'Cannot wire {o} (type={type(o)}) to {i.debug_name} (type={type(i)}) because conversions from IntegerTypes are only defined for Bits, not general Arrays', debug_info=debug_info)  # noqa
            else:
                o_str = getattr(o, "debug_name", str(o))
                _logger.error(f'Cannot wire {o_str} (type={type(o)}) to {i.debug_name} (type={type(i)}) because {o_str} is not an Array', debug_info=debug_info)  # noqa
            return

        if i.N != o.N:
            _logger.error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because the arrays do not have the same length', debug_info=debug_info)  # noqa
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

        return type(self).flip()(*ts)

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if self.iswhole(ts):
            return ts[0].name.array

        return type(self).flip()(*ts)

    def const(self):
        for t in self.ts:
            if not t.const():
                return False

        return True

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

    def as_bits(self):
        if isinstance(self.T, Digital):
            return Bits[len(self)](self.ts)
        return reduce(lambda x, y: x.concat(y),
                      map(lambda x: x.as_bits(), self.ts))

    @classmethod
    def from_bits(cls, value):
        if issubclass(cls.T, Digital):
            if not len(cls) == len(value):
                raise TypeError("Width mismatch")
            return cls(value.ts)
        child_length = cls.T.flat_length()
        children = [
            cls.T.from_bits(
                value[i * child_length:(i + 1) * child_length]
            )
            for i in range(child_length)
        ]
        return cls(children)

    @classmethod
    def is_mixed(cls):
        return cls.T.is_mixed()



ArrayType = Array
