from magma.passes.passes import DefinitionPass
from magma.wire_clock import wiredefaultclock, wireclock


class WireClockPass(DefinitionPass):
    def __call__(self, definition):
        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            wireclock(definition, instance)
