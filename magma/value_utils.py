import dataclasses
import typing

from magma.ref import Ref, TupleRef, ArrayRef
from magma.type_utils import (isprotocol, isdigital, isbits, isarray, istuple,
                              GenericWrapper, WrappedVisitor)


def _unwrap_protocol_value(value):
    T = type(value)
    if isprotocol(T):
        return value._get_magma_value_()
    return value


@dataclasses.dataclass(frozen=True)
class _ValueWrapper(GenericWrapper):
    pass


def _wrap_value(value):
    if isinstance(value, _ValueWrapper):
        return value
    value = _unwrap_protocol_value(value)
    T = type(value)

    if isdigital(T):
        return _ValueWrapper(value, [], "Digital")
    if isbits(T):
        return _ValueWrapper(value, [], "Bits")
    if isarray(T):
        return _ValueWrapper(value, [t for t in value], "Array")
    if istuple(T):
        return _ValueWrapper(value, [t for t in value], "Tuple")

    raise NotImplementedError(T)


class ValueVisitor(WrappedVisitor):
    def wrap(self, value):
        return _wrap_value(value)


@dataclasses.dataclass(frozen=True)
class Selector:
    child: 'Selector'

    def select(self, value):
        value = self._select(value)
        if self.child is None:
            return value
        return self.child.select(value)

    def _select(self, value):
        return value

    def _child_str(self):
        return "" if self.child is None else str(self.child)


@dataclasses.dataclass(frozen=True)
class TupleSelector(Selector):
    key: str

    def _select(self, value):
        return getattr(value, self.key)

    def __str__(self):
        return f".{self.key}{self._child_str()}"


@dataclasses.dataclass(frozen=True)
class ArraySelector(Selector):
    index: int

    def _select(self, value):
        return value[self.index]

    def __str__(self):
        return f"[{self.index}]{self._child_str()}"


def _make_selector_impl(value, child):
    value = _unwrap_protocol_value(value)
    ref = value.name
    if isinstance(ref, ArrayRef):
        child = ArraySelector(child, ref.index)
        return _make_selector_impl(ref.array, child)
    if isinstance(ref, TupleRef):
        child = TupleSelector(child, ref.index)
        return _make_selector_impl(ref.tuple, child)
    if child is not None:
        return child
    return Selector(None)


def make_selector(value):
    return _make_selector_impl(value, None)
