import functools
from typing import Iterable, Mapping

from magma.array import Array
from magma.circuit import Circuit, DefineCircuitKind
from magma.clock import (
    ClockTypes, Clock, Reset, Enable, ResetN, AsyncReset, AsyncResetN)
from magma.common import (
    only, IterableException, EmptyIterableException,
    NonSignletonIterableException)
from magma.logging import root_logger
from magma.primitives.wire import Wire
from magma.t import Type, Kind
from magma.tuple import Tuple
from magma.wire import wire


_logger = root_logger()


def _get_output_clocks_in_array(
        value: Array, clock_type: Kind) -> Iterable[Type]:
    """
    Gets all output values of type @clock_type recursively contained in @value.
    """
    first_clks = get_output_clocks_in_value(value[0], clock_type)
    try:
        first_clk = next(first_clks)
    except StopIteration:  # early exit to avoid traversing children
        return None
    yield first_clk
    yield from first_clks
    for elem in value[1:]:
        yield from get_output_clocks_in_value(elem, clock_type)


def get_output_clocks_in_value(value: Type, clock_type: Kind) -> Iterable[Type]:
    """
    Gets all output values of type @clock_type recursively contained in @value.
    """
    # Since we are looking for default drivers, only need to consider outputs.
    if value.is_input():
        return None
    if isinstance(value, clock_type):
        yield value
    if isinstance(value, Tuple):
        for elem in value:
            yield from get_output_clocks_in_value(elem, clock_type)
    if isinstance(value, Array):
        yield from _get_output_clocks_in_array(value, clock_type)


def get_output_clocks_in_defn(
        defn: DefineCircuitKind, clock_type: Kind) -> Iterable[Type]:
    """
    Gets all output values of type @clock_type in circuit @defn. This includes
    "input" ports of @defn and output ports of any instances contained in @defn.
    """
    for port in defn.interface.ports.values():
        yield from get_output_clocks_in_value(port, clock_type)
    for inst in defn.instances:
        if isinstance(type(inst), Wire):
            # We want to skip instances of Wire(T), because they are basically
            # buffers and therefore their outputs are not legitimate
            # drivers. Not doing so might result in spurrious "multiple clocks".
            continue
        for port in inst.interface.ports.values():
            yield from get_output_clocks_in_value(port, clock_type)


def get_all_output_clocks_in_defn(
        defn: DefineCircuitKind) -> Mapping[Kind, Type]:
    """
    Returns a map from each clock type to either the singleton output value of
    that type in @defn, or None (if there is none, or there are multiple).
    """
    default_clocks = {}
    for clock_type in ClockTypes:
        clocks = get_output_clocks_in_defn(defn, clock_type)
        try:
            clock = only(clocks)
        except IterableException:
            clock = None
        default_clocks[clock_type] = clock
    return default_clocks


def drive_undriven_clocks_in_value(
        value: Type, clock_type: Kind, driver: Type) -> bool:
    """
    Drives all undriven values of type @clock_type contained in @value with
    @driver. Returns whether any such values were driven by @driver.
    """
    if isinstance(value, Tuple):
        has_undriven = False
        for elem in value:
            elem_has_undriven = drive_undriven_clocks_in_value(
                elem, clock_type, driver)
            has_undriven |= elem_has_undriven
        return has_undriven
    if isinstance(value, Array):
        # First check if the first element has any undriven.
        has_undriven = drive_undriven_clocks_in_value(
            value[0], clock_type, driver)
        # Only traverse all children circuit if first child has a clock.
        if not has_undriven:
            return False
        # TODO(leonardt): Magma doesn't supvalue length zero array, so slicing a
        # length 1 array off the end doesn't work as expected in normal Python,
        # so we explicilty slice value.ts.
        for t in value.ts[1:]:
            for elem in value[1:]:
                drive_undriven_clocks_in_value(elem, clock_type, driver)
        return True
    if isinstance(value, clock_type) and value.trace() is None:
        # Trace back to last undriven driver.
        while value.driven():
            value = value.value()
        _logger.info(f"Auto-wiring {repr(driver)} to {repr(value)}")
        value @= driver
        return True
    return False


def drive_undriven_clocks_in_inst(
        defn: DefineCircuitKind, inst: Circuit, clock_type: Kind):
    """
    Drives all undriven input ports of @inst of type @clock_type with a default
    driver of type @clock_type contained in @defn. If no such default driver
    exists (either due to no drivers or multiple drivers existing), then this
    function is a no-op.
    """
    clks = get_output_clocks_in_defn(defn, clock_type)
    try:
        clk = only(clks)
    except EmptyIterableException:
        _logger.warning(
            f"Found no clocks in {defn.name}; skipping auto-wiring "
            f"{clock_type}")
        return
    except NonSignletonIterableException:
        _logger.warning(
            f"Found multiple clocks in {defn.name}; skipping auto-wiring "
            f"{clock_type}")
        return
    for port in inst.interface.inputs(include_clocks=True):
        drive_undriven_clocks_in_value(port, clock_type, clk)


def drive_all_undriven_clocks_in_value(
        value: Type, clocks: Mapping[Kind, Type]) -> bool:
    """
    Drives all undriven input values contained in @value for each of the (clock
    type, default driver) pairs in @clocks.
    """
    has_undriven = False
    for clock_type, clk in clocks.items():
        if clk is None:
            continue
        has_undriven |= drive_undriven_clocks_in_value(value, clock_type, clk)
    return has_undriven


def drive_undriven_clock_types_in_inst(defn: DefineCircuitKind, inst: Circuit):
    drive_undriven_clocks_in_inst(defn, inst, Clock)


def drive_undriven_other_clock_types_in_inst(
        defn: DefineCircuitKind, inst: Circuit):
    drive_undriven_clocks_in_inst(defn, inst, Reset)
    drive_undriven_clocks_in_inst(defn, inst, ResetN)
    drive_undriven_clocks_in_inst(defn, inst, AsyncReset)
    drive_undriven_clocks_in_inst(defn, inst, AsyncResetN)
    drive_undriven_clocks_in_inst(defn, inst, Enable)
