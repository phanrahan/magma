import abc
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
class GenericWrapper:
    raw: typing.Any
    children: typing.List[typing.Any]
    name: str


class WrappedVisitor:
    def visit(self, node):
        wrapped = self.wrap(node)
        method = 'visit_' + wrapped.name
        visitor = getattr(self, method, self.generic_visit)
        return visitor(wrapped.raw)

    def generic_visit(self, node):
        wrapped = self.wrap(node)
        for child in wrapped.children:
            self.visit(child)

    @abc.abstractmethod
    def wrap(self, node):
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class _TypeWrapper(GenericWrapper):
    attrs: typing.Dict[str, typing.Any]
    constructor: typing.Callable


def _wrap_type(T):
    if isinstance(T, _TypeWrapper):
        return T
    T = _unwrap_protocol_type(T)

    if isdigital(T):
        return _TypeWrapper(T, [], "Digital", {}, lambda T: T)
    if isbits(T):
        return _TypeWrapper(T, [], "Bits", {}, lambda T: T)
    if isarray(T):

        def _constructor(T, subT):
            return T[T.N, subT]

        return _TypeWrapper(T, [T.T], "Array", {"N": T.N}, _constructor)
    if istuple(T):

        def _constructor(T, *args):
            field_dict = {key: arg
                          for key, arg in zip(T.field_dict.keys(), args)
                          if arg is not None}
            unbound = _get_unbound_root(T)
            return unbound.from_fields(T.__name__, field_dict)

        attrs = {"fields": T.field_dict}
        children = list(T.field_dict.values())
        return _TypeWrapper(T, children, "Tuple", attrs, _constructor)

    raise NotImplementedError(T)


class TypeVisitor(WrappedVisitor):
    def wrap(self, T):
        return _wrap_type(T)


class TypeTransformer(TypeVisitor):
    def generic_visit(self, T):
        wrapped = _wrap_type(T)
        args = (self.visit(child) for child in wrapped.children)
        return wrapped.constructor(T, *args)
