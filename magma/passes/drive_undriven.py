from .passes import EditCircuitPass


def _drive_undriven(interface):
    undriven = False
    for port in interface.ports.values():
        if port.is_input() and port.trace() is None:
            undriven = True
            port.undriven()
    return undriven


class DriveUndrivenPass(EditCircuitPass):
    def edit(self, circuit):
        if _drive_undriven(circuit.interface):
            circuit._is_definition = True
        for inst in circuit.instances:
            _drive_undriven(inst.interface)
