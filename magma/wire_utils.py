from typing import Union

from magma.t import Type
from magma.view import PortView
from magma.primitives.xmr import XMRSink, XMRSource


ValueOrPortView = Union[Type, PortView]


class WiringError(Exception):
    pass


def wire_value_or_driver(drivee: Type, driver: Type):
    assert drivee.is_input()
    if driver.is_input():
        value = driver.value()
        if value is None:
            raise WiringError(drivee, driver)
        drivee @= value
    elif driver.is_mixed():
        for drivee_i, driver_i in zip(drivee, driver):
            wire_value_or_driver(drivee_i, driver_i)
    else:
        drivee @= driver


def wire_value_or_port_view(drivee: Type, value_or_port_view: ValueOrPortView):
    if isinstance(value_or_port_view, PortView):
        defn = value_or_port_view.parent_view.inst.defn
        with defn.open():
            xmr_sink = XMRSink(value_or_port_view)()
            wire_value_or_driver(xmr_sink.I, value_or_port_view.port)
        xmr_source = XMRSource(value_or_port_view)()
        wire_value_or_driver(drivee, xmr_source.O)
        return
    wire_value_or_driver(drivee, value_or_port_view)
