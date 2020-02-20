from abc import abstractmethod
from .passes import DefinitionPass


class IgnoreErrorsPass(DefinitionPass):
    def __init__(self, main, placer_block):
        super().__init__(main)
        self.placer_block = placer_block

    @abstractmethod
    def ignore(self, port_values):
        raise NotImplementedError()

    def __call__(self, definition):
        with self.placer_block(definition._placer):
            self.ignore(definition.interface.ports.values())
            for instance in definition.instances:
                self.ignore(instance.interface.ports.values())



class IgnoreUndrivenPass(IgnoreErrorsPass):
    def ignore(self, port_values):
        for value in port_values:
            if value.is_input() and value.trace() is None:
                value.undriven()


class IgnoreUnusedPass(IgnoreErrorsPass):
    def ignore(self, port_values):
        for value in port_values:
            if value.is_output() and value.wired() is False:
                value.unused()
