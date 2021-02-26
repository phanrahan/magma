import enum
import functools
from typing import Optional

from magma.circuit import CircuitKind
from magma.value_utils import ValueVisitor


class StubType(enum.Enum):
    ZERO = enum.auto()


class _StubifyVisitor(ValueVisitor):
    def __init__(self, stub_type: StubType):
        self._stub_type = stub_type
        self._modified = False

    @property
    def modified(self):
        return self._modified

    def _handle_value(self, value):
        self._modified = True
        if not value.is_input():
            value.unused()
            return
        if self._stub_type is StubType.ZERO:
            value @= 0
            return
        raise NotImplementedError(self._stub_type)

    def visit_Bits(self, value):
        self._handle_value(value)

    def visit_Digital(self, value):
        self._handle_value(value)


def _stubify_impl(ckt: CircuitKind, stub_type: StubType):
    modified = False
    for port in ckt.interface.ports.values():
        visitor = _StubifyVisitor(stub_type)
        visitor.visit(port)
        modified |= visitor.modified
    if modified:
        # NOTE(rsetaluri): This is a hack because we don't have good handling of
        # isdefinition when the circuit is modified. We should be doing that
        # more principled-ly. See https://github.com/phanrahan/magma/issues/929.
        ckt._is_definition = True


def stubify(ckt: CircuitKind, stub_type: StubType):
    with ckt.open():
        _stubify_impl(ckt, stub_type)


def circuit_stub(cls=None, *, stub_type: Optional[StubType] = StubType.ZERO):
    """
    Inspired by https://pybit.es/decorator-optional-argument.html.

    Stub-ifys a circuit, based on optional parameter @stub_type. Default
    behavior is driving all outputs to zero. All inputs will be marked as unused
    automatically as well.
    """
    if cls is None:
        return partial(circuit_stub, stub_type=stub_type)
    stubify(cls, stub_type)
    return cls
