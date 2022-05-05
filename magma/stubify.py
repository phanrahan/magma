import functools
from typing import Callable, Iterable

from magma.circuit import CircuitKind, CircuitType, DefineCircuitKind
from magma.conversions import as_bits
from magma.value_utils import ValueVisitor
from magma.t import Type


Stubbifier = Callable[[Type], bool]


def zero_stubbifier(value: Type) -> bool:
    if value.is_output():
        value.unused()
        return True
    if value.is_input():
        bits = as_bits(value)
        bits @= 0
        return True
    return False


class _StubifyVisitor(ValueVisitor):
    def __init__(self, stubbifier: Stubbifier):
        self._stubbifier = stubbifier
        self._modified = False

    @property
    def modified(self):
        return self._modified

    def generic_visit(self, value: Type):
        modified = self._stubbifier(value)
        if modified:
            self._modified = True
            return
        super().generic_visit(value)


def _stubify_impl(
        ports: Iterable[Type],
        stubbifier: Stubbifier = zero_stubbifier
) -> bool:
    modified = False
    for port in ports:
        visitor = _StubifyVisitor(stubbifier)
        visitor.visit(port)
        modified = modified or visitor.modified
    return modified


def _stub_open(cls):
    raise NotImplementedError("Can not call open() on a circuit stub")


@functools.singledispatch
def stubify(interface, stubbifier: Stubbifier = zero_stubbifier):
    _ = _stubify_impl(interface.ports.values(), stubbifier)


@stubify.register
def _(obj: CircuitKind, stubbifier: Stubbifier = zero_stubbifier):
    ckt = obj
    with ckt.open():
        modified = _stubify_impl(ckt.interface.ports.values(), stubbifier)
    if modified:
        # NOTE(rsetaluri): This is a hack because we don't have good handling of
        # isdefinition when the circuit is modified. We should be doing that
        # more principled-ly. See https://github.com/phanrahan/magma/issues/929.
        ckt._is_definition = True
    # Set ckt.open to be a function which raises a NotImplementedError. Note
    # that we *can't* do this in the class itself, since we need to call open()
    # to tie the outputs first (in stubify()). Afterwards, we can override the
    # method.
    setattr(ckt, "open", classmethod(_stub_open))


def circuit_stub(cls=None, *, stubbifier: Stubbifier = zero_stubbifier):
    """
    Inspired by https://pybit.es/decorator-optional-argument.html.

    Stub-ifys a circuit, based on optional parameter @stubbifier. Default
    behavior is driving all outputs to zero. All inputs will be marked as unused
    automatically as well.
    """
    if cls is None:
        return partial(circuit_stub, stubbifier=stubbifier)
    stubify(cls, stubbifier)
    return cls


class _CircuitStubMeta(DefineCircuitKind):
    def __new__(metacls, name, bases, dct):
        cls = super().__new__(metacls, name, bases, dct)
        # Only call stubify() on user circuits (i.e. do not call on CircuitStub
        # base class).
        if not dct.get("_circuit_base_", False):
            stubify(cls, stubbifier=zero_stubbifier)
        return cls


class CircuitStub(CircuitType, metaclass=_CircuitStubMeta):
    _circuit_base_ = True
