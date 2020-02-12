from functools import lru_cache
import weakref
import magma as m
from abc import ABCMeta
from .t import Kind, Direction, Type
from .debug import debug_wire, get_callee_frame_info
from .compatibility import IntegerTypes
from .logging import root_logger
from .port import Port


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
            if isinstance(value, (bool, IntegerTypes)):
                return m.VCC if value else m.GND
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
            o = m.HIGH if o else m.LOW

        if not isinstance(o, Digital):
            _logger.error(f'Cannot wire {i.debug_name} (type={type(i)}) to {o} '
                          f'(type={type(o)}) because {o.debug_name} is not a '
                          f'Digital', debug_info=debug_info)
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
        return self is m.VCC or self is m.GND

    def unwire(i, o):
        i.port.unwire(o.port)

    @classmethod
    def flat_length(cls):
        return 1

    # Loam methods, TODO: rework this interface
    def getinst(self):
        t = self.trace()
        return t.name.inst if t is not None else None

    def getgpio(self):
        return self.getinst()

    def unused(self):
        if not self.is_output():
            raise TypeError("unused can only be used on output")
        m.wire(self, DefineUnused()().I)

    def undriven(self):
        if not self.is_input():
            raise TypeError("undriven can only be used on input")
        m.wire(DefineUndriven()().O, self)


def make_Define(name, port, direction):
    def simulate(self, value_store, state_store):
        pass

    @lru_cache(maxsize=None)
    def DefineCorebit():
        return m.circuit.DeclareCoreirCircuit(
            f"corebit_{name}",
            port, direction(Digital),
            coreir_name=name,
            coreir_lib="corebit",
            simulate=simulate
        )
    return DefineCorebit


DefineUndriven = make_Define("undriven", "O", m.Out)
DefineUnused = make_Define("term", "I", m.In)
