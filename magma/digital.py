from functools import lru_cache
import weakref
from abc import ABCMeta
import hwtypes as ht
from .t import Kind, Direction, Type, In, Out
from .debug import debug_wire, get_callee_frame_info
from .compatibility import IntegerTypes
from .logging import root_logger
from .protocol_type import magma_type, magma_value

from magma.wire_container import Wire, WiringLog


_logger = root_logger()


class DigitalMeta(ABCMeta, Kind):
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
            # class is unundirected so t.unundirected_t -> t
            type_._info_ = type_, direction
        elif info[0] is None:
            # class inherited from directed types so there is no unundirected_t
            type_._info_ = None, direction

        if not type_.is_directed:
            type_.VCC = type_[Direction.Out](name="VCC")
            type_.GND = type_[Direction.Out](name="GND")

        return type_

    def __getitem__(cls, direction: Direction) -> 'DigitalMeta':
        mcs = type(cls)
        try:
            return mcs._class_cache[cls, direction]
        except KeyError:
            pass

        if not isinstance(direction, Direction):
            raise TypeError('Direction of Digital must be an instance of '
                            'm.Direction')

        if cls.is_directed:
            if direction == direction.Undirected:
                return cls.undirected_t
            if direction == cls.direction:
                return cls
            else:
                return cls.undirected_t[direction]
        if direction == direction.Undirected:
            return cls

        bases = [cls]
        bases.extend(b[direction] for b in cls.__bases__ if isinstance(b, mcs))
        bases = tuple(bases)
        orig_name = cls.__name__
        class_name = '{}[{}]'.format(orig_name, direction.name)
        type_ = mcs(class_name, bases, {"orig_name": orig_name},
                    info=(cls, direction))
        type_.__module__ = cls.__module__
        mcs._class_cache[cls, direction] = type_
        return type_

    def __call__(cls, value=None, *args, **kwargs):
        if value is not None:
            if isinstance(value, (bool, IntegerTypes, ht.Bit)):
                return cls.VCC if value else cls.GND
        result = super().__call__(*args, **kwargs)
        if value is not None:
            if not isinstance(value, Digital):
                raise TypeError(type(value))
            result(value)
        return result

    def __repr__(cls):
        return str(cls)

    def __str__(cls):
        name = getattr(cls, "orig_name", cls.__name__)
        if cls.is_input():
            name = f"In({name})"
        elif cls.is_output():
            name = f"Out({name})"
        elif cls.is_inout():
            name = f"InOut({name})"
        return name

    @property
    def undirected_t(cls) -> 'DigitalMeta':
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

    def qualify(cls, direction):
        return cls[direction]

    def __eq__(cls, rhs):
        return isinstance(rhs, DigitalMeta)

    def is_wireable(cls, rhs):
        if issubclass(rhs, (bool, int, ht.Bit)):
            return True
        rhs = magma_type(rhs)
        # allows undirected types to match (e.g. for temporary values)
        return (issubclass(rhs.flip(), cls) or issubclass(cls, rhs.flip()) or
                cls.qualify(Direction.Undirected) is rhs or
                rhs.qualify(Direction.Undirected) is cls)

    def is_bindable(cls, rhs):
        return issubclass(cls, magma_type(rhs))

    __hash__ = type.__hash__


class Digital(Type, metaclass=DigitalMeta):
    def __init__(self, value=None, name=None):
        super().__init__(name=name)
        self._wire = Wire(self)

    @classmethod
    def is_oriented(cls, direction):
        if not cls.is_directed:
            return direction == Direction.Undirected
        return cls.direction == direction

    @classmethod
    def is_clock(cls):
        return False

    def __call__(self, output):
        return self.wire(output, get_callee_frame_info())

    @debug_wire
    def wire(self, o, debug_info):
        i = self
        o = magma_value(o)
        # promote integer types to LOW/HIGH
        if isinstance(o, (IntegerTypes, bool, ht.Bit)):
            o = HIGH if o else LOW

        if not isinstance(o, Digital):
            _logger.error(
                WiringLog(f"Cannot wire {{}} (type={type(i)}) to {o} "
                          f"(type={type(o)}) because {{}} is not a Digital",
                          i, o),
                debug_info=debug_info
            )
            return

        i._wire.connect(o._wire, debug_info)
        i.debug_info = debug_info
        o.debug_info = debug_info

    def iswhole(self):
        return True

    def wired(self):
        return self._wire.wired()

    # return the input or output Bit connected to this Bit
    def trace(self):
        return self._wire.trace()

    # return the output Bit connected to this input Bit
    def value(self):
        return self._wire.value()

    def driven(self):
        return self._wire.driven()

    def driving(self):
        return self._wire.driving()

    @classmethod
    def unflatten(cls, value):
        if len(value) != 1 or not isinstance(value[0], Digital):
            raise TypeError("Can only convert from Bits[1] to Bit")
        return value[0]

    def flatten(self):
        return [self]

    def const(self):
        cls = type(self)
        return self is cls.VCC or self is cls.GND

    def unwire(i, o):
        i._wire.unwire(o._wire)

    @classmethod
    def flat_length(cls):
        return 1

    # Loam methods, TODO: rework this interface
    def getinst(self):
        t = self.trace()
        return t.name.inst if t is not None else None

    def getgpio(self):
        return self.getinst()

    @classmethod
    def is_mixed(cls):
        return False

    def __repr__(self):
        cls = type(self)
        if self is cls.VCC:
            return "VCC"
        if self is cls.GND:
            return "GND"
        return Type.__repr__(self)


VCC = Digital.VCC
GND = Digital.GND

HIGH = VCC
LOW = GND
