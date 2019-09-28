import weakref
import typing as tp
import enum
from abc import ABCMeta
import functools
from hwtypes.bit_vector_abc import AbstractBit, TypeFamily
from .debug import debug_wire
from .compatibility import IntegerTypes
from .port import report_wiring_error, Port


class Direction(enum.Enum):
    In = 0
    Out = 1
    InOut = 2
    Flip = 3


def bit_cast(fn: tp.Callable[['Bit', 'Bit'], 'Bit']) -> \
        tp.Callable[['Bit', tp.Union['Bit', bool]], 'Bit']:
    @functools.wraps(fn)
    def wrapped(self: 'Bit', other: tp.Union['Bit', bool]) -> 'Bit':
        if isinstance(other, Bit):
            return fn(self, other)
        try:
            other = Bit(other)
        except TypeError:
            return NotImplemented
        return fn(self, other)
    return wrapped


class BitMeta(ABCMeta):
    # BitVectorType, size :  BitVectorType[size]
    _class_cache = weakref.WeakValueDictionary()

    def __new__(cls, name, bases, namespace, info=(None, None), **kwargs):
        # TODO: A lot of this code is shared with AbstractBitVectorMeta, we
        # should refactor to reuse
        if '_info_' in namespace:
            raise TypeError(
                'class attribute _info_ is reversed by the type machinery')

        direction = info[1]
        for base in bases:
            if getattr(base, 'is_directed', False):
                if direction is None:
                    direction = base.direction
                elif direction != base.direction:
                    raise TypeError(
                        "Can't inherit from multiple different directions")

        namespace['_info_'] = info[0], direction
        type_ = super().__new__(cls, name, bases, namespace, **kwargs)
        if direction is None:
            #class is unundirected so t.unundirected_t -> t
            type_._info_ = type_, direction
        elif info[0] is None:
            #class inherited from directed types so there is no unundirected_t
            type_._info_ = None, direction

        return type_

    def __getitem__(cls, direction: Direction) -> 'AbstractBitVectorMeta':
        mcs = type(cls)
        try:
            return mcs._class_cache[cls, direction]
        except KeyError:
            pass

        if not isinstance(direction, Direction):
            raise TypeError('Direction of Bit must be an instance of m.Direction')

        if cls.is_directed:
            if direction == cls.direction:
                return cls
            elif direction == direction.Flip:
                if cls.direction == direction.In:
                    return cls[direction.Out]
                elif cls.direction == direction.Out:
                    return cls[direction.In]
                else:
                    # Flip of inout is inout
                    return cls
            else:
                return cls.undirected_t[direction]

        bases = [cls]
        bases.extend(b[direction] for b in cls.__bases__ if isinstance(b, mcs))
        bases = tuple(bases)
        class_name = '{}[{}]'.format(cls.__name__, direction)
        type_ = mcs(class_name, bases, {}, info=(cls, direction))
        type_.__module__ = cls.__module__
        mcs._class_cache[cls, direction] = type_
        return type_

    @property
    def undirected_t(cls) -> 'BitMeta':
        t = cls._info_[0]
        if t is not None:
            return t
        else:
            raise AttributeError('type {} has no undirected_t'.format(cls))

    @property
    def direction(cls) -> int:
        return cls._info_[1]

    @property
    def is_directed(cls) -> bool:
        return cls.direction is not None

    def __len__(cls):
        return 1

    def __str__(cls):
        if cls.is_directed:
            return f"Bit[{cls.direction.name}]"
        return "Bit"


class Bit(AbstractBit, metaclass=BitMeta):
    @staticmethod
    def get_family() -> TypeFamily:
        # TODO: We'll probably have a circular dependency issue if types are
        # defined in separate files, we could monkey patch a field in __init__
        # after the files are loaded
        raise NotImplementedError()
        return _Family_

    def __init__(self, value=None, name=None):
        self.name = name
        # TODO: Port debug_name code
        self.debug_name = name
        if value is None:
            self._value = None
        elif isinstance(value, Bit):
            self._value = value._value
        elif isinstance(value, bool):
            self._value = value
        elif isinstance(value, int):
            if value not in {0, 1}:
                raise ValueError('Bit must have value 0 or 1 not {}'.format(value))
            self._value = bool(value)
        elif hasattr(value, '__bool__'):
            self._value = bool(value)
        else:
            raise TypeError("Can't coerce {} to Bit".format(type(value)))
        self.port = Port(self)

    def __invert__(self):
        return self.__invert()(self)

    @bit_cast
    def __eq__(self, other):
        return self.__eq(self, other)

    @bit_cast
    def __ne__(self, other):
        return self.__ne(self, other)

    @bit_cast
    def __and__(self, other):
        return self.__and(self, other)

    @bit_cast
    def __or__(self, other):
        return self.__or(self, other)

    @bit_cast
    def __xor__(self, other):
        return self.__xor(self, other)

    def ite(self, t_branch, f_branch):
        # TODO: This is basically just a phi/mux, but if we need this func we
        # can patch the same implementation in
        raise NotImplementedError()

    def __bool__(self) -> bool:
        # Don't think we can suppor this in magma
        raise NotImplementedError()

    def __int__(self) -> int:
        # Don't think we can suppor this in magma
        raise NotImplementedError()

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return 'Bit({})'.format(self._value)

    def __repr__(self) -> str:
        return 'Bit({})'.format(self._value)

    # def __hash__(self) -> int:
    #     return hash(self._value)

    def is_input(self):
        return type(self).direction == Direction.In

    def is_output(self):
        return type(self).direction == Direction.Out

    def is_inout(self):
        return type(self).direction == Direction.InOut

    @debug_wire
    def wire(self, o, debug_info):
        i = self
        # promote integer types to LOW/HIGH
        if isinstance(o, IntegerTypes):
            o = HIGH if o else LOW

        if not isinstance(o, Bit):
            report_wiring_error(f'Cannot wire {i.debug_name} (type={type(i)}) to {o} (type={type(o)}) because {o.debug_name} is not a Bit', debug_info)
            return

        i.port.wire(o.port, debug_info)
        i.debug_info = debug_info
        o.debug_info = debug_info

    def anon(self):
        return self.name is None

    def wired(self):
        return self.port.wired()

    # return the input or output Bit connected to this Bit
    def trace(self):
        t = self.port.trace()
        if t:
            t = t.bit
        return t

    # return the output Bit connected to this input Bit
    def value(self):
        t = self.port.value()
        if t:
            t = t.bit
        return t


In = Direction.In
Out = Direction.Out
Flip = Direction.Flip
BitIn = Bit[In]
BitOut = Bit[Out]
VCC = BitOut(1, name="VCC")
GND = BitOut(0, name="GND")

HIGH = VCC
LOW = GND
