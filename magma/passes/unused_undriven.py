from abc import abstractmethod
from .passes import CircuitPass


class UndrivenUnusedPass(CircuitPass):
    @abstractmethod
    def process(self, port_values):
        raise NotImplementedError()

    def __call__(self, circuit):
        with circuit.open():
            self.process(circuit.interface.ports.values())
            for instance in circuit.instances:
                self.process(instance.interface.ports.values())


class DriveUndriven(UndrivenUnusedPass):
    def process(self, port_values):
        for value in port_values:
            if value.is_input() and value.trace() is None:
                value.undriven()


class TerminateUnused(UndrivenUnusedPass):
    def process(self, port_values):
        for value in port_values:
            if value.is_output() and value.wired() is False:
                value.unused()
