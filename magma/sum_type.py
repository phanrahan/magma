from typing import Optional

from magma.bits import Bits
from magma.bitutils import clog2
from magma.common import Stack
from magma.protocol_type import MagmaProtocol, MagmaProtocolMeta
from magma.t import Type, Direction, Kind
from magma.tuple import AnonProduct
from magma.conversions import from_bits, as_bits, zext_to
from magma.when import when, elsewhen, otherwise


class SumMeta(MagmaProtocolMeta):
    def _to_magma_(cls):
        return cls._magma_T_

    def _qualify_magma_(cls, direction: Direction):
        dct = {"_magma_T_": cls._magma_T_.qualify(direction)}
        for k, v in cls._magma_Ts_.items():
            dct[k] = v.qualify(direction)
        return type(cls)(cls.__name__, (cls, ), dct)

    def _flip_magma_(cls):
        dct = {"_magma_T_": cls._magma_T_.flip()}
        for k, v in cls._magma_Ts_.items():
            dct[k] = v.flip()
        return type(cls)(cls.__name__, (cls, ), dct)

    def _from_magma_value_(cls, val: Type):
        return cls(val)

    def __new__(mcs, name, bases, namespace):
        data_len = 0
        Ts = {}
        # TODO(leonardt/sum): How to handle mixed direction type?
        is_input, is_output = True, True

        for key, value in namespace.items():
            if key.startswith("_magma_"):
                continue
            if isinstance(value, Kind):
                data_len = max(data_len, value.flat_length())
                Ts[key] = value
                is_input &= value.is_input()
                is_output &= value.is_output()
        if len(Ts):
            assert data_len > 0, "Expected non zero length data"

            tag_len = clog2(len(Ts))
            T = AnonProduct[
                {"tag": Bits[tag_len], "data": Bits[data_len]}
            ]
            if is_input:
                T = T.qualify(Direction.In)
            elif is_output:
                T = T.qualify(Direction.Out)
            namespace['_magma_T_'] = T
            namespace['_magma_Ts_'] = Ts
            namespace['_magma_TagMap_'] = {}

        return type.__new__(mcs, name, bases, namespace)


class Sum(MagmaProtocol, metaclass=SumMeta):
    def __init__(self, val: Optional[Type] = None):
        if val is None:
            val = self._magma_T_()
        self._val = val

        self._tag_map = {}  # map from T to int id value
        if self._magma_TagMap_:
            self._tag_map = self._magma_TagMap_
        else:
            for T in self._magma_Ts_.values():
                # For now, tags map to index in _magma_Ts_ order.
                self._tag_map[T.undirected_t] = len(self._tag_map)

        self._match_active = False  # must be True to use case
        self._active_case = None  # tracks current case type
        self._activated_cases = []  # tracks prev activated cases

    @property
    def match_active(self):
        return self._match_active

    @match_active.setter
    def match_active(self, value):
        self._match_active = value

    @property
    def activated_cases(self):
        return self._activated_cases

    @property
    def num_tags(self):
        return len(self._tag_map)

    def _check_case_type(self, T):
        if T.undirected_t not in self._tag_map:
            raise TypeError(f"Unexpected case type {T}")

    def activate_case(self, T):
        if self._active_case is not None:
            raise TypeError("Cannot have more than one active case")
        if any(T is x for x in self._activated_cases):
            raise TypeError(f"Cannot call case({T}) twice")
        self._check_case_type(T)

        self._active_case = T
        self._activated_cases.append(T)

    def deactivate_case(self):
        last_T = self._active_case
        self._active_case = None
        return last_T

    def _get_magma_value_(self):
        if self._active_case:
            # Interpret base on active case T
            T = self._active_case.undirected_t
            return from_bits(T, self._val.data[:T.flat_length()])
        return self._val

    def check_tag(self, T):
        # Used for when condition in a specific case.
        return self._val.tag == self._tag_map[T]

    def __invert__(self):
        return ~self._get_magma_value_()

    def __xor__(self, other):
        return self._get_magma_value_() ^ other

    def __and__(self, other):
        return self._get_magma_value_() & other

    # TODO(leonardt/sum): define all operators (can we metaprogram delegator to
    # self._get_magma_value_()?)

    def _get_tag(self, driver):
        try:
            return self._tag_map[type(driver).undirected_t]
        except KeyError:
            raise TypeError(f"Cannot wire {driver} to {self}")

    def wire(self, other):
        if self._active_case:
            self._get_magma_value_().wire(other)
            return
        self._val.tag @= self._get_tag(other)
        if hasattr(self._val, "data"):
            self._val.data @= zext_to(as_bits(other), len(self._val.data))


_MATCH_STACK = Stack()


def reset_match_context():
    _MATCH_STACK.clear()


class MatchContext:
    """
    Marks a value of type Sum to be inside an active match context, enabling
    the use of case statements.
    """

    def __init__(self, value):
        self._value = value
        _MATCH_STACK.push(self)

    @property
    def value(self):
        return self._value

    def __enter__(self):
        self._value.match_active = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        assert self._value.match_active, "Should not have been deactivated"
        assert _MATCH_STACK.pop() is self
        self._value.match_active = False


match = MatchContext


class CaseContext:
    """
    Reinterprets a value of type Sum as a specific variant indicated by the
    case statement argument and resets the value when the context is exited
    """

    def __init__(self, T):
        try:
            value = _MATCH_STACK.peek().value
        except IndexError:
            raise TypeError("Case used outside of match statement")
        assert value.match_active

        self._value = value
        self._T = T
        # Use elsewhen/otherwise to avoid latch detect issues
        # TODO(leonardt/sum): Enforce that this isn't interleaved with other
        # when/case statements
        if len(self._value.activated_cases) == self._value.num_tags - 1:
            self._when_ctx = otherwise()
        elif self._value.activated_cases:
            self._when_ctx = elsewhen(value.check_tag(T))
        else:
            self._when_ctx = when(value.check_tag(T))

    def __enter__(self):
        self._value.activate_case(self._T)
        self._when_ctx.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        last_T = self._value.deactivate_case()
        assert last_T is self._T, "Got wrong expected activate case"
        self._when_ctx.__exit__(exc_type, exc_value, exc_tb)


case = CaseContext


class Enum2Meta(SumMeta):
    def __new__(mcs, name, bases, namespace):
        tag_len = 0
        for key, value in namespace.items():
            if isinstance(value, int):
                tag_len = max(tag_len, value.bit_length())

        if tag_len:
            tag_map = {}
            T = AnonProduct[{"tag": Bits[tag_len]}]
            for key, value in namespace.items():
                if isinstance(value, int):
                    namespace[key] = value = T(Bits[tag_len](value))
                    tag_map[value] = value.tag
            namespace['_magma_T_'] = T
            namespace['_magma_Ts_'] = {}
            namespace['_magma_TagMap_'] = tag_map

        return type.__new__(mcs, name, bases, namespace)


class Enum2(Sum, metaclass=Enum2Meta):
    def _get_tag(self, driver):
        return self._tag_map[driver]

    def _check_case_type(self, value):
        if not isinstance(value, Type):
            raise TypeError(f"Unexpected case value {value}")
