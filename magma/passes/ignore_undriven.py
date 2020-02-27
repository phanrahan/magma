from .passes import DefinitionPass


class IgnoreUndrivenPass(DefinitionPass):
    def __init__(self, main, placer_block):
        super().__init__(main)
        self.placer_block = placer_block

    def ignore_undriven(self, port_values):
        for value in port_values:
            if value.is_input() and value.trace() is None:
                value.undriven()

    def __call__(self, definition):
        with self.placer_block(definition._placer):
            self.ignore_undriven(definition.interface.ports.values())
            for instance in definition.instances:
                self.ignore_undriven(instance.interface.ports.values())
