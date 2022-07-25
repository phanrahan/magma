from magma.circuit import CircuitBuilder
from magma.t import Out, In
from magma.definition_context import DefinitionContext


def _get_conditional_values(context):
    conditional_values = set()
    for cond in context.when_conds:
        for key in cond.conditional_wires.keys():
            conditional_values.add(key)
    return list(sorted(conditional_values, key=lambda x: str(x.name)))


class ConditionalDriver(CircuitBuilder):
    def __init__(self, context):
        super().__init__("_magma_conditional_driver_" + str(id(context)))
        self._conditional_drivers = {}
        self._debug_info = {}
        self._when_conds = []
        self._reverse_map = {}
        self._cond_map = {}

    def add_when_cond(self, cond):
        self._when_conds.append(cond)

    @property
    def when_conds(self):
        return [x for x in self._when_conds if x.has_conditional_wires()]

    @property
    def conditional_values(self):
        return list(self._conditional_drivers.keys())

    def get_debug_info(self, value, cond):
        return self._debug_info[value][cond]

    def make_conditional_output(self, value):
        name = str(value.name)
        self._reverse_map[value] = name
        self._conditional_drivers[value] = {}
        self._debug_info[value] = {}
        self._add_port(name, Out(type(value)))
        return getattr(self, name)

    def remove(self, value):
        for key, driver in self._conditional_drivers[value].items():
            if key is None:
                continue
            key[-1].remove_conditional_wire(value)
        del self._conditional_drivers[value]
        del self._debug_info[value]
        # Just leave ports for now, but we could remove them

    def _add_missing_conds(self, conds, debug_info):
        for cond in conds:
            if cond in self._cond_map:
                continue
            cond_value = cond.cond
            if getattr(cond_value, 'is_otherwise_cond', False):
                continue
            cond_name = str(cond_value.name)
            self._add_port(cond_name, In(type(cond_value)))
            getattr(self, cond_name).unconditional_wire(cond_value, debug_info)
            self._reverse_map[cond_value] = cond_name

    def add_conditional_driver(self, target, value, cond, debug_info):
        """
        For the case when a driven value is conditionally driven in a
        subsequent when statement, e.g.

        x @= y  # default driver
        m.when(z):
            x @= w

        The special case condition `None` is used to identify the default
        driver in `self._conditional_drivers`
        """
        self._conditional_drivers[target][cond] = value
        self._debug_info[target][cond] = debug_info
        cond_name = str(target.name) + "_"
        if cond is not None:
            self._add_missing_conds(cond, debug_info)
        else:
            cond_name += "None"

        value_name = cond_name + "_" + str(value.name)
        self._add_port(value_name, In(type(value)))
        getattr(self, value_name).unconditional_wire(value, debug_info)
        self._reverse_map[value] = value_name

        if cond is not None:
            cond[-1].add_conditional_wire(target, value, debug_info)

    def _finalize(self):
        self._dct['_is_conditional_driver_'] = True
        self._dct['conditional_values'] = self.conditional_values
        self._dct['conditional_drivers'] = self._conditional_drivers
        self._dct['reverse_map'] = self._reverse_map
        self._dct['when_conds'] = self.when_conds


DefinitionContext._make_conditional_driver = lambda self: ConditionalDriver(self)
