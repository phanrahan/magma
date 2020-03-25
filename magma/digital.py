from functools import lru_cache
import weakref
import magma as m
from abc import ABCMeta
from .t import Kind, Direction, Type, In, Out
from .debug import debug_wire, get_callee_frame_info
from .compatibility import IntegerTypes
from .logging import root_logger


_logger = root_logger()


class Wire:
    """
    Wire implements wiring.

    Each wire is represented by a bit.
    """
    def __init__(self, bit):
        self.bit = bit
        self.driving = []
        self.driver = None

    def __repr__(self):
        return repr(self.bit)

    def __str__(self):
        return str(self.bit)

    def anon(self):
        return self.bit.anon()

    def unwire(self, other):
        other.driving.remove(self)
        self.driver = None

    def connect(self, other, debug_info):
        """
        Connect two wires, self should be an input and other should be an
        output, or both should be inouts
        """
        if self.driver is not None and self.bit.is_input():
            _logger.warning(
                "Wiring multiple outputs to same wire, using last connection."
                f" Input: {self.bit.debug_name}, "
                f" Old Output: {self.driver.bit.debug_name}, "
                f" New Output: {other.bit.debug_name}",
                debug_info=debug_info
            )
        if self.bit.is_output():
            _logger.error(f"Using `{self.bit.debug_name}` (an output) as an "
                          f"input", debug_info=debug_info)
            return
        if other.bit.is_input():
            _logger.error(f"Using `{other.bit.debug_name}` (an input) as an "
                          f"output", debug_info=debug_info)
            return
        if self.bit.is_inout() and not other.bit.is_inout():
            _logger.error(f"Using `{other.bit.debug_name}` (not inout) as an "
                          f"inout", debug_info=debug_info)
            return
        if not self.bit.is_inout() and other.bit.is_inout():
            _logger.error(f"Using `{self.bit.debug_name}` (not inout) as an "
                          f"inout", debug_info=debug_info)
            return

        self.driver = other
        other.driving.append(self)

    def trace(self, skip_self=True):
        """
        If a value is an input or an intermediate (undirected), trace it until
        there is an input or inout (this is the source)

        Upon the first invocation (from a user), we skip the current bit (so
        we don't trace to ourselves)
        """
        if self.driver is not None:
            return self.driver.trace(skip_self=False)
        if not skip_self and (self.bit.is_output() or self.bit.is_inout()):
            return self.bit
        return None

    def value(self):
        """
        Return the driver of this wire
        """
        if self.bit.is_output():
            raise TypeError("Can only get value of non outputs")
        if self.driver is None:
            return None
        return self.driver.bit

    def driven(self):
        return self.trace() is not None

    def wired(self):
        return self.driver or self.driving


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

    def __eq__(cls, rhs):
        return cls is rhs

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

    def __call__(self, output):
        return self.wire(output, get_callee_frame_info())

    @debug_wire
    def wire(self, o, debug_info):
        i = self
        # promote integer types to LOW/HIGH
        if isinstance(o, IntegerTypes):
            o = HIGH if o else LOW

        if not isinstance(o, Digital):
            _logger.error(f'Cannot wire {i.debug_name} (type={type(i)}) to {o} '
                          f'(type={type(o)}) because {o.debug_name} is not a '
                          f'Digital', debug_info=debug_info)
            return

        i._wire.connect(o._wire, debug_info)
        i.debug_info = debug_info
        o.debug_info = debug_info

    def iswhole(self, _):
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

    def flatten(self):
        return [self]

    def const(self):
        return self is VCC or self is GND

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

    def unused(self):
        if self.is_input() or self.is_inout():
            raise TypeError("unused cannot be used with input/inout")
        m.wire(m.bit(self), DefineUnused()().I)

    def undriven(self):
        if self.is_output() or self.is_inout():
            raise TypeError("undriven cannot be used with output/inout")
        m.wire(DefineUndriven()().O, m.bit(self))

    @classmethod
    def is_mixed(cls):
        return False

    def __repr__(self):
        if self is VCC:
            return "VCC"
        if self is GND:
            return "GND"
        return Type.__repr__(self)


def make_Define(_name, port, direction):
    @lru_cache(maxsize=None)
    def DefineCorebit():
        class _Primitive(m.Circuit):
            renamed_ports = m.circuit.coreir_port_mapping
            name = f"corebit_{_name}"
            coreir_name = _name
            coreir_lib = "corebit"

            def simulate(self, value_store, state_store):
                pass

            # Type must be a bit because coreir uses Bit for the primitive,
            # insert_wrap_casts will handle the conversion of other digital
            # types like Clock
            io = m.IO(**{port: direction(m.Bit)})
        return _Primitive
    return DefineCorebit


VCC = Digital[Direction.Out](name="VCC")
GND = Digital[Direction.Out](name="GND")

HIGH = VCC
LOW = GND

DefineUndriven = make_Define("undriven", "O", Out)
DefineUnused = make_Define("term", "I", In)
