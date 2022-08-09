from typing import Optional

from magma.bits import Bits
from magma.bitutils import clog2
from magma.protocol_type import MagmaProtocol, MagmaProtocolMeta
from magma.t import Type, Direction, Kind
from magma.tuple import AnonProduct
from magma.conversions import from_bits, as_bits, zext_to
from magma.when import WhenCtx, _OtherwiseCond, _check_prev_when_cond


class SumMeta(MagmaProtocolMeta):
    def _to_magma_(cls):
        return cls._magma_T_

    def _qualify_magma_(cls, direction: Direction):
        dct = {k: v.qualify(direction)
               for k, v in cls._magma_Ts_.items()}
        return type(cls)(cls.__name__, (cls, ), dct)

    def _flip_magma_(cls):
        dct = {k: v.flip()
               for k, v in cls._magma_Ts_.items()}
        return type(cls)(cls.__name__, (cls, ), dct)

    def _from_magma_value_(cls, val: Type):
        return cls(val)

    def __new__(mcs, name, bases, namespace):
        data_len = 0
        Ts = {}
        # TODO: How to handle mixed direction type?
        is_input, is_output = True, True

        for key, value in namespace.items():
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

        return type.__new__(mcs, name, bases, namespace)


class Sum(MagmaProtocol, metaclass=SumMeta):
    def __init__(self, val: Optional[Type] = None):
        if val is None:
            val = self._magma_T_()
        self._val = val

        self._tag_map = {}  # map from T to int id value
        for T in self._magma_Ts_.values():
            # For now, tags map to index in _magma_Ts_ order
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

    def activate_case(self, T):
        if self._active_case is not None:
            raise TypeError("Cannot have more than one active case")
        if T in self._activated_cases:
            raise TypeError(f"Cannot call case({T}) twice")
        if T.undirected_t not in self._tag_map:
            raise TypeError(f"Unexpected case type {T}")

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
        # Used for when condition in a specific case
        return self._val.tag == self._tag_map[T]

    def __invert__(self):
        return ~self._get_magma_value_()

    def __xor__(self, other):
        return ~self._get_magma_value_() ^ other

    # TODO: define all operators (can we metaprogram delegator to
    # self._get_magma_value_()?)

    def wire(self, other):
        T = type(other).undirected_t
        if T not in self._tag_map:
            raise TypeError(f"Cannot wire {other} to {self}")
        self._val.tag @= self._tag_map[T]
        self._val.data @= zext_to(as_bits(other), len(self._val.data))


class MatchContext:
    """
    Marks a value of type Sum to be inside an active match context, enabling
    the use of case statements.
    """

    def __init__(self, value):
        self._value = value

    def __enter__(self):
        self._value.match_active = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        assert self._value.match_active, "Should not have been deactivated"
        self._value.match_active = False


match = MatchContext


class CaseContext(WhenCtx):
    """
    Reinterprets a value of type Sum as a specific variant indicated by the
    case statement argument and resets the value when the context is exited
    """

    def __init__(self, value, T):
        if not value.match_active:
            raise TypeError(f"Using case({value}, {T}) requires an enclosing "
                            "match statement")
        self._value = value
        self._T = T
        if len(self._value._activated_cases) == len(self._value._tag_map) - 1:
            # Use otherwise to avoid latch detect
            super().__init__(_OtherwiseCond(),
                             _check_prev_when_cond('otherwise'))
        else:
            super().__init__(value.check_tag(T))

    def __enter__(self):
        self._value.activate_case(self._T)
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, exc_tb):
        last_T = self._value.deactivate_case()
        assert last_T is self._T, "Got wrong expected activate case"
        return super().__exit__(exc_type, exc_value, exc_tb)


case = CaseContext
