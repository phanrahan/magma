import dataclasses
import functools
import itertools
from typing import Optional

from magma.clock import is_clock_or_nested_clock, ClockTypes
from magma.compile_exception import make_unconnected_error_str
from magma.debug import debug_info as debug_info_cls
from magma.logging import root_logger
from magma.t import Type
from magma.wire_container import WiringLog


_logger = root_logger()


@dataclasses.dataclass(frozen=True)
class UnconnectedPortInfo:
    port: Type
    debug_info: Optional[debug_info_cls]


def find_unconnected_ports_of_port(port, debug_info):
    if port.is_output():
        return
    if port.is_inout() and port.wired():
        # TODO(leonardt/rsetaluri): Ideally, we should trace in both directions
        # for an inout; for now we assume that if it's "wired()", then it is
        # connected.
        return
    if port.is_mixed():
        for elt in port:
            yield from find_unconnected_ports_of_port(elt, debug_info)
        return
    if port.trace() is None:
        # If we encounter a clock, issue a debug message that we are not
        # counting this as an unconnected port and instead will attempt to
        # automatically wire it downstream.
        if isinstance(port, ClockTypes):
            msg = "{} not driven, will attempt to automatically wire"
            _logger.debug(WiringLog(msg, port), debug_info=debug_info)
            return
        # If there is a clock nested in @port, then we need to traverse its
        # children. Note that although we use is_clock_or_nested_clock here,
        # because of the preceding check for ClockTypes, this conditional will
        # only catch the nested clock case.
        if is_clock_or_nested_clock(type(port)):
            for elt in port:
                yield from find_unconnected_ports_of_port(elt, debug_info)
            return
        yield UnconnectedPortInfo(port, debug_info)
        return
    return


def find_unconnected_ports_of_interface(interface, debug_info):
    for port in interface.ports.values():
        yield from find_unconnected_ports_of_port(port, debug_info)


def find_unconnected_ports_of_circuit(ckt):
    yield from find_unconnected_ports_of_interface(
        ckt.interface, ckt.debug_info
    )
    for inst in ckt.instances:
        yield from find_unconnected_ports_of_interface(
            inst.interface, inst.debug_info
        )


@dataclasses.dataclass
class UnconnectedPortDiagnostic:
    value: Type
    connected: Optional[bool]
    depth: int

    def make_wiring_log(self) -> str:
        tab = " " * (4 * self.depth)
        connected_str = ""
        if self.connected is True:
            connected_str = ": Connected"
        elif self.connected is False:
            connected_str = ": Unconnected"
        tpl = f"{tab}{{}}{connected_str}"
        return WiringLog(tpl, self.value)


# NOTE(rsetaluri): The value visitor class for constructing the unconnected port
# diagnostic info requires inheriting from ValueVisitor (defined in
# magma/value_utils.py). This would result in a cyclical import dependency. To
# hack around this issue, the value visitor class is created in a factory which
# should only run once, and use the cached result for future invocations. Note
# that we set @maxsize to 1 for the lru cache.
@functools.lru_cache(maxsize=1)
def _make_unconnected_port_diagnostic_visitor_cls():
    from magma.value_utils import ValueVisitor

    class _Visitor(ValueVisitor):
        def __init__(self):
            self._depth = 0

        def visit(self, node):
            yield from super().visit(node)

        def generic_visit(self, value):
            if value.trace() is not None:
                yield UnconnectedPortDiagnostic(value, True, self._depth)
                return
            wrapped = self.wrap(value)
            results = []
            has_connected = False
            self._depth += 1
            for child in wrapped.children:
                for diagnostic in self.visit(child):
                    has_connected = has_connected or diagnostic.connected
                    results.append(diagnostic)
            self._depth -= 1
            if not has_connected:
                yield UnconnectedPortDiagnostic(value, False, self._depth)
                return
            yield UnconnectedPortDiagnostic(value, None, self._depth)
            yield from iter(results)

    return _Visitor


def find_and_log_unconnected_ports(ckt):
    infos = find_unconnected_ports_of_circuit(ckt)
    for info in infos:
        port = info.port
        debug_info = info.debug_info
        _logger.error(WiringLog("{} not driven", port), debug_info=debug_info)
        visitor = _make_unconnected_port_diagnostic_visitor_cls()()
        diagnostics = visitor.visit(port)
        for diagnostic in diagnostics:
            _logger.error(diagnostic.make_wiring_log())
