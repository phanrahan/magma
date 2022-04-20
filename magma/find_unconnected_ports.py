import dataclasses
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


def check_unconnected(ckt):
    unconnected_ports = find_unconnected_ports_of_circuit(ckt)
    for unconnected_port in unconnected_ports:
        port = unconnected_port.port
        debug_info = unconnected_port.debug_info
        msg = "{} not driven\n\nUnconnected port info"
        msg += "\n---------------------\n    "
        error_msg, format_args = make_unconnected_error_str(port)
        msg += "\n    ".join(error_msg.splitlines())
        _logger.error(WiringLog(msg, port, *format_args),
                      debug_info=debug_info)
        ckt._has_errors_ = True
