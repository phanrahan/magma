import itertools
from typing import Iterable, Mapping

from magma.array import Array
from magma.circuit import Circuit, DefineCircuitKind
from magma.clock import (
    ClockTypes, Clock, Reset, Enable, ResetN, AsyncReset, AsyncResetN,
    is_clock_or_nested_clock)
from magma.common import (
    only, IterableException, EmptyIterableException,
    NonSingletonIterableException)
from magma.logging import root_logger
from magma.passes.passes import DefinitionPass, pass_lambda
from magma.primitives.wire import Wire
from magma.t import Type, Kind
from magma.tuple import Tuple


_logger = root_logger()


def _get_output_clocks_in_array(
        value: Array, clock_type: Kind) -> Iterable[Type]:
    """
    Gets all output values of type @clock_type recursively contained in @value.
    """
    if not is_clock_or_nested_clock(type(value).T, (clock_type, )):
        return None
    for elem in value:
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


def _get_undriven_clocks_in_array(
        value: Array, clock_type: Kind) -> Iterable[Type]:
    """
    Returns all undriven values of type @clock_type contained in array @value.
    """
    # First check if the first element has any undriven.
    it = get_undriven_clocks_in_value(value[0], clock_type)
    try:
        first = next(it)
    except StopIteration:  # early exit to avoid traversing other elements
        return
    yield first
    yield from it
    # NOTE(rsetaluri): Since magma does not allow zero-length arrays, we need to
    # check that the length of the array is > 1 before slicing it with [1:].
    if len(value) <= 1:
        return
    for elem in value[1:]:
        yield from get_undriven_clocks_in_value(elem, clock_type)


def get_undriven_clocks_in_value(
        value: Type, clock_type: Kind) -> Iterable[Type]:
    """Returns all undriven values of type @clock_type contained in @value."""
    if not is_clock_or_nested_clock(type(value), (clock_type, )):
        # Avoid descening into tuple/array if possible
        return
    if isinstance(value, Tuple):
        for elem in value:
            yield from get_undriven_clocks_in_value(elem, clock_type)
        return
    if isinstance(value, Array):
        yield from _get_undriven_clocks_in_array(value, clock_type)
        return
    if isinstance(value, clock_type) and value.trace() is None:
        # Trace back to last undriven driver.
        while value.driven():
            value = value.value()
        yield value
    return


def _drive_value_with_clock(value: Type, clk: Type):
    _logger.debug(f"Auto-wiring {repr(clk)} to {repr(value)}")
    value @= clk


def drive_undriven_clocks_in_inst(
        defn: DefineCircuitKind, inst: Circuit, clock_type: Kind):
    """
    Drives all undriven input ports of @inst of type @clock_type with a default
    driver of type @clock_type contained in @defn. If no such default driver
    exists (either due to no drivers or multiple drivers existing), then this
    function is a no-op.
    """
    undrivens = iter(())
    for port in inst.interface.inputs(include_clocks=True):
        undrivens = itertools.chain(
            undrivens, get_undriven_clocks_in_value(port, clock_type))

    try:
        undriven = next(undrivens)
    except StopIteration:
        return
    clks = get_output_clocks_in_defn(defn, clock_type)
    try:
        clk = only(clks)
    except EmptyIterableException:
        _logger.warning(
            f"Found no clocks in {defn.name}; skipping auto-wiring "
            f"{clock_type}")
        return
    except NonSingletonIterableException as e:
        _logger.warning(
            f"Found multiple clocks in {defn.name}; skipping auto-wiring "
            f"{clock_type} ({', '.join(map(repr, e.args[0]))})"
        )
        return
    # Restore undrivens after popping off the first element.
    undrivens = itertools.chain([undriven], undrivens)
    for undriven in undrivens:
        _drive_value_with_clock(undriven, clk)


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
        undrivens = get_undriven_clocks_in_value(value, clock_type)
        for undriven in undrivens:
            has_undriven = True
            _drive_value_with_clock(undriven, clk)
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


class WireClockPass(DefinitionPass):
    def __call__(self, definition):
        with definition.open():
            for instance in definition.instances:
                drive_undriven_clock_types_in_inst(definition, instance)
                drive_undriven_other_clock_types_in_inst(definition, instance)


wire_clocks = pass_lambda(WireClockPass)
