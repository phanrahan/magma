import weakref
from abc import ABCMeta
from .t import Kind, Direction, Type
from .debug import debug_wire, get_callee_frame_info
from .port import report_wiring_error, Port
from .compatibility import IntegerTypes


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
        orig_name = cls.__name__
        class_name = '{}[{}]'.format(orig_name, direction.name)
        type_ = mcs(class_name, bases, {"orig_name": orig_name},
                    info=(cls, direction))
        type_.__module__ = cls.__module__
        mcs._class_cache[cls, direction] = type_
        return type_

    def __call__(cls, value=None, *args, **kwargs):
        if value is not None:
            if isinstance(value, (bool, IntegerTypes)):
                return VCC if value else GND
        result = super().__call__(*args, **kwargs)
        if value is not None:
            assert isinstance(value, Digital), type(value)
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

    def flip(cls):
        return cls.qualify(Direction.Flip)

    def __eq__(cls, rhs):
        return cls is rhs

    __hash__ = type.__hash__


class Digital(Type, metaclass=DigitalMeta):
    def __init__(self, value=None, name=None):
        super().__init__(name=name)
        self.port = Port(self)

    @classmethod
    def is_oriented(cls, direction):
        return cls.direction == direction

    def __call__(self, output):
        return self.wire(output, get_callee_frame_info())

    @debug_wire
    def wire(self, o, debug_info):
        i = self
        # promote integer types to LOW/HIGH
        if isinstance(o, IntegerTypes):
            o = HIGH if o else LOW

        if not isinstance(o, Digital):
            report_wiring_error(f'Cannot wire {i.debug_name} (type={type(i)}) '
                                f'to {o} (type={type(o)}) because '
                                f'{o.debug_name} is not a Digital', debug_info)
            return

        i.port.wire(o.port, debug_info)
        i.debug_info = debug_info
        o.debug_info = debug_info

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

    def driven(self):
        return self.port.driven()

    def flatten(self):
        return [self]

    def const(self):
        return self is VCC or self is GND

    def unwire(i, o):
        i.port.unwire(o.port)

    @classmethod
    def flat_length(cls):
        return 1


VCC = Digital[Direction.Out](name="VCC")
GND = Digital[Direction.Out](name="GND")

HIGH = VCC
LOW = GND
