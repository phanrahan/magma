from .passes import EditCircuitPass


def _terminate_unused(interface):
    terminated = False
    for port in interface.ports.values():
        if port.is_output() and port.wired() is False:
            terminated = True
            port.unused()
    return terminated


class TerminateUnusedPass(EditCircuitPass):
    def edit(self, circuit):
        if _terminate_unused(circuit.interface):
            circuit._is_definition = True
        for inst in circuit.instances:
            _terminate_unused(inst.interface)
