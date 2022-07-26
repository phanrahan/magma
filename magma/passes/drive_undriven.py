from magma.array import Array
from magma.clock import is_clock_or_nested_clock
from magma.is_definition import isdefinition
from magma.passes.clock import (
    drive_all_undriven_clocks_in_value,
    get_all_output_clocks_in_defn,
)
from magma.passes.passes import EditDefinitionPass, pass_lambda
from magma.tuple import Tuple


def _drive_undriven_children(port, clocks):
    # list comp so it doesn't short circuit
    undrivens = [_drive_if_undriven_input(p, clocks) for p in port]
    return any(undrivens)


def _drive_if_undriven_input(port, clocks):
    if port.is_mixed():
        return _drive_undriven_children(port, clocks)
    if port.is_input() and port.trace() is None:
        if (isinstance(port, (Array, Tuple)) and
                any(t.trace() is not None for t in port)):
            # Partially undriven, recurse through to drive only the undriven
            # children
            return _drive_undriven_children(port, clocks)
        if (not is_clock_or_nested_clock(type(port)) or
                not drive_all_undriven_clocks_in_value(port, clocks)):
            port.undriven()
        # We always return True, even if we do default clock wiring since in
        # this case, it should be a definition now
        return True
    return False


def _drive_undriven(interface, clocks):
    undriven = False
    for port in interface.ports.values():
        undriven |= _drive_if_undriven_input(port, clocks)
    return undriven


class DriveUndrivenPass(EditDefinitionPass):
    def edit(self, circuit):
        clocks = get_all_output_clocks_in_defn(circuit)
        if _drive_undriven(circuit.interface, clocks):
            circuit._is_definition = True
        if not isdefinition(circuit):
            return
        for inst in circuit.instances:
            _drive_undriven(inst.interface, clocks)


drive_undriven = pass_lambda(DriveUndrivenPass)
