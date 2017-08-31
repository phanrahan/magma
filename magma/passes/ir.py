from .passes import DefinitionPass
from .clock import WireClockPass

class IRPass(DefinitionPass):
    def __init__(self, main):
        super(IRPass, self).__init__(main)
        self.code = ''

        WireClockPass(main).run()

    def __call__(self, definition):
        self.code += repr(definition) + '\n\n'
