from typing import Optional

from magma.bits import Bits
from magma.protocol_type import MagmaProtocol, MagmaProtocolMeta
from magma.t import Type, Direction, Kind
from magma.conversions import from_bits


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
        N = 0
        Ts = {}
        for key, value in namespace.items():
            if isinstance(value, Kind):
                N = max(N, value.flat_length())
                Ts[key] = value
        if N > 0:
            namespace['_magma_T_'] = Bits[N]
            namespace['_magma_Ts_'] = Ts

        return type.__new__(mcs, name, bases, namespace)


class Sum(MagmaProtocol, metaclass=SumMeta):
    def __init__(self, val: Optional[Type] = None):
        if val is None:
            val = self._magma_T_()
        self._val = val
        for key, T in self._magma_Ts_.items():
            setattr(self, key,
                    from_bits(T, val[:T.flat_length()]))


def match(value, field):
    print(value, field)
    raise Exception()
