import abc

from magma.debug import debug_wire


class MagmaProtocolMeta(type):
    @abc.abstractmethod
    def _to_magma_(cls):
        # To retrieve underlying magma type.
        raise NotImplementedError()

    @abc.abstractmethod
    def _qualify_magma_(cls, direction: 'Direction'):
        # To qualify underlying type (e.g. give me a Foo with the underlying
        # type qualified to be an input).
        raise NotImplementedError()

    @abc.abstractmethod
    def _flip_magma_(cls):
        # To flip underlying type (e.g. give me a Foo with the underlying type
        # flipped).
        raise NotImplementedError()

    def qualify(cls, direction: 'Direction'):
        return cls._qualify_magma_(direction)

    @abc.abstractmethod
    def _from_magma_value_(cls, val: 'Type'):
        # To create an instance from a value.
        raise NotImplementedError()

    @abc.abstractmethod
    def _is_oriented_magma_(cls, direction):
        raise NotImplementedError()

    def is_oriented(cls, direction):
        return cls._is_oriented_magma_(direction)

    def flip(cls):
        return cls._flip_magma_()

    def __len__(cls):
        return len(cls._to_magma_())

    def is_wireable(cls, rhs):
        return cls._to_magma_().is_wireable(rhs)

    def is_bindable(cls, rhs):
        return cls._to_magma_().is_bindable(rhs)


class MagmaProtocol(metaclass=MagmaProtocolMeta):
    @abc.abstractmethod
    def _get_magma_value_(self):
        # To access underlying magma value.
        raise NotImplementedError()

    @classmethod
    def is_clock(cls):
        return cls._to_magma_().is_clock()

    @classmethod
    def is_inout(cls):
        return cls._to_magma_().is_inout()

    @classmethod
    def is_input(cls):
        return cls._to_magma_().is_input()

    @classmethod
    def is_mixed(cls):
        return cls._to_magma_().is_mixed()

    @classmethod
    def is_output(cls):
        return cls._to_magma_().is_output()

    def iswhole(self):
        return self._get_magma_value_().iswhole()

    def value(self):
        return self._get_magma_value_().value()

    def trace(self):
        return self._get_magma_value_().trace()

    def driven(self):
        return self._get_magma_value_().driven()

    def flatten(self):
        return self._get_magma_value_().flatten()

    def __iter__(self):
        return iter(self._get_magma_value_())

    @property
    def name(self):
        return self._get_magma_value_().name

    @debug_wire
    def wire(self, other, debug_info):
        if isinstance(other, MagmaProtocol):
            other = other._get_magma_value_()
        self._get_magma_value_().wire(other, debug_info)

    def unwire(self, other):
        if isinstance(other, MagmaProtocol):
            other = other._get_magma_value_()
        self._get_magma_value_().unwire(other)

    def __imatmul__(self, other):
        self.wire(other)
        return self


def magma_type(T):
    if issubclass(T, MagmaProtocol):
        return T._to_magma_()
    return T


def magma_value(value):
    if isinstance(value, MagmaProtocol):
        return value._get_magma_value_()
    return value
