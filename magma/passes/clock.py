from magma.passes.passes import DefinitionPass
from magma.wire_clock import (
    drive_undriven_clock_types_in_inst,
    drive_undriven_other_clock_types_in_inst)


class WireClockPass(DefinitionPass):
    def __call__(self, definition):
        for instance in definition.instances:
            drive_undriven_clock_types_in_inst(definition, instance)
            drive_undriven_other_clock_types_in_inst(definition, instance)
