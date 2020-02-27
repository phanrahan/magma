from abc import abstractmethod
from .passes import EditCircuitPass


class UndrivenUnusedPass(EditCircuitPass):
    def __call__(self, circuit):
        with circuit.open():
            self.process(circuit, circuit.interface.ports.values())
            for instance in circuit.instances:
                self.process(circuit, instance.interface.ports.values())


def _drive_undriven(interface):
    undriven = False
    for port in interface.ports.values():
        if port.is_input() and port.trace() is None:
            undriven = True
            port.undriven()
    return undriven


def _terminate_unused(interface):
    terminated = False
    for port in interface.ports.values():
        if port.is_output() and port.wired() is False:
            terminated = True
            port.unused()
    return terminated


class DriveUndrivenPass(EditCircuitPass):
    def edit(self, circuit):
        if _drive_undriven(circuit.interface):
            circuit._is_definition = True
        for inst in circuit.instances:
            _drive_undriven(inst.interface)


class TerminateUnusedPass(EditCircuitPass):
    def edit(self, circuit):
        if _terminate_unused(circuit.interface):
            circuit._is_definition = True
        for inst in circuit.instances:
            _terminate_unused(inst.interface)
