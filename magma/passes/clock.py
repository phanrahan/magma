from ..is_definition import isdefinition
from ..clock import wiredefaultclock, wireclock
from .passes import DefinitionPass

__all__ = ['WireClockPass']


class WireClockPass(DefinitionPass):
    def __call__(self, definition):
        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            wireclock(definition, instance)
