import enum
import functools
from typing import Optional

from magma.circuit import CircuitKind, CircuitType, DefineCircuitKind
from magma.conversions import as_bits
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

    def _drive_output(self, value):
        if self._stub_type == StubType.ZERO:
            bits = as_bits(value)
            bits @= 0
            return
        raise NotImplementedError(self._stub_type)

    def _handle_value(self, value, leaf=False):
        if value.is_output():
            self._modified = True
            value.unused()
            return
        if value.is_input():
            self._modified = True
            self._drive_output(value)
            return
        if leaf:
            return
        super().generic_visit(value)

    def generic_visit(self, value):
        self._handle_value(value, leaf=False)

    def visit_Bits(self, value):
        self._handle_value(value, leaf=True)

    def visit_Digital(self, value):
        self._handle_value(value, leaf=True)


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


def _stub_open(cls):
    raise NotImplementedError("Can not call open() on a circuit stub")


def stubify(ckt: CircuitKind, stub_type: StubType):
    with ckt.open():
        _stubify_impl(ckt, stub_type)
    # Set ckt.open to be a function which raises a NotImplementedError. Note
    # that we *can't* do this in the class itself, since we need to call open()
    # to tie the outputs first (in stubify()). Afterwards, we can override the
    # method.
    setattr(ckt, "open", classmethod(_stub_open))


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


class _CircuitStubMeta(DefineCircuitKind):
    def __new__(metacls, name, bases, dct):
        cls = super().__new__(metacls, name, bases, dct)
        # Only call stubify() on user circuits (i.e. do not call on CircuitStub
        # base class).
        if not dct.get("_circuit_base_", False):
            stubify(cls, stub_type=StubType.ZERO)
        return cls


class CircuitStub(CircuitType, metaclass=_CircuitStubMeta):
    _circuit_base_ = True
