from .clock import WireClockPass
from .passes import DefinitionPass


class IRPass(DefinitionPass):
    def __init__(self, main):
        super().__init__(main)
        self.code = ""

        WireClockPass(main).run()

    def __call__(self, definition):
        self.code += repr(definition) + "\n\n"
