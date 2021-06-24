from ..is_definition import isdefinition
from ..wire_clock import wiredefaultclock, wireclock
from .passes import DefinitionPass


class WireClockPass(DefinitionPass):
    def __call__(self, definition):
        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            wireclock(definition, instance)


class RemoveDefaultClockIfUnused(DefinitionPass):
    def __call__(self, definition):
        if definition.io.has_default_clock:
            for instance in definition.instances:
                wiredefaultclock(definition, instance)
                wireclock(definition, instance)
            if not definition.CLK.driving():
                definition.interface.remove("CLK")
