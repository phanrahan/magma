import dataclasses
import typing

from magma.array import Array
from magma.bits import Bits, UInt, SInt
from magma.digital import Digital
from magma.protocol_type import MagmaProtocol
from magma.tuple import Tuple


def isprotocol(T):
    return issubclass(T, MagmaProtocol)


def isdigital(T):
    return issubclass(T, Digital)


def isbits(T):
    return issubclass(T, Bits)


def isarray(T):
    return issubclass(T, Array)


def istuple(T):
    return issubclass(T, Tuple)


def isuint(T):
    return issubclass(T, UInt)


def issint(T):
    return issubclass(T, SInt)


def _unwrap_protocol_type(T):
    if isprotocol(T):
        return T._to_magma_()
    return T


def _get_unbound_root(T):
    types = [T]
    while types:
        T = types.pop(0)
        if T._unbound_base_ is not None and not T._unbound_base_.is_bound:
            return T._unbound_base_
        types += T.__bases__


@dataclasses.dataclass(frozen=True)
class _TypeWrapper:
    raw: typing.Any
    children: typing.List[typing.Any]
    attrs: typing.Dict[str, typing.Any]
    constructor: typing.Callable
    name: str


def _wrap_type(T):
    if isinstance(T, _TypeWrapper):
        return T
    T = _unwrap_protocol_type(T)

    if isdigital(T):
        constructor = lambda T: T
        return _TypeWrapper(T, [], {}, constructor, "Digital")
    if isbits(T):
        constructor = lambda T: T
        return _TypeWrapper(T, [], {}, constructor, "Bits")
    if isarray(T):
        constructor = lambda T, subT: T[T.N, subT]
        return _TypeWrapper(T, [T.T], {"N": T.N}, constructor, "Array")
    if istuple(T):

        def _constructor(T, *args):
            field_dict = {list(T.field_dict.keys())[i]: args[i]
                          for i in range(len(T.field_dict))}
            field_dict = {k: v for k, v in field_dict.items() if v is not None}
            unbound = _get_unbound_root(T)
            return unbound.from_fields(T.__name__, field_dict)

        attrs = {"fields": T.field_dict}
        children = [value for value in T.field_dict.values()]
        return _TypeWrapper(T, children, attrs, _constructor, "Tuple")

    raise NotImplementedError(T)


class TypeVisitor:
    def visit(self, T):
        wrapped = _wrap_type(T)
        method = 'visit_' + wrapped.name
        visitor = getattr(self, method, self.generic_visit)
        return visitor(wrapped.raw)

    def generic_visit(self, T):
        wrapped = _wrap_type(T)
        for child in wrapped.children:
            self.visit(child)


class TypeTransformer(TypeVisitor):
    def generic_visit(self, T):
        wrapped = _wrap_type(T)
        args = [self.visit(child) for child in wrapped.children]
        return wrapped.constructor(T, *args)
