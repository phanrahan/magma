from .passes import EditDefinitionPass
from ..is_definition import isdefinition


def _drive_if_undriven_input(port):
    if port.is_mixed():
        # Sum so it doesn't short circuit
        return sum(_drive_if_undriven_input(p) for p in port)
    if port.is_input() and port.trace() is None:
        port.undriven()
        return True
    return False


def _drive_undriven(interface):
    undriven = False
    for port in interface.ports.values():
        undriven |= _drive_if_undriven_input(port)
    return undriven


class DriveUndrivenPass(EditDefinitionPass):
    def edit(self, circuit):
        if _drive_undriven(circuit.interface):
            circuit._is_definition = True
        if not isdefinition(circuit):
            return
        for inst in circuit.instances:
            _drive_undriven(inst.interface)
