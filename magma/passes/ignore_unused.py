from .passes import DefinitionPass


class IgnoreUnusedPass(DefinitionPass):
    def __init__(self, main, placer_block):
        super().__init__(main)
        self.placer_block = placer_block

    def ignore_unused(self, port_values):
        for value in port_values:
            if value.is_output() and value.wired() is False:
                value.unused()

    def __call__(self, definition):
        with self.placer_block(definition._placer):
            self.ignore_unused(definition.interface.ports.values())
            for instance in definition.instances:
                self.ignore_unused(instance.interface.ports.values())
