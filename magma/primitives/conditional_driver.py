from magma.circuit import CircuitBuilder
from magma.t import Out, In
from magma.definition_context import DefinitionContext


class ConditionalDriver(CircuitBuilder):
    def __init__(self, context):
        """
        `_conditionally_driven_info`: mapping from values to a dictionary
                                      containing a mapping from conditions to
                                      conditional_driver

                                      i.e. Dict[Type, Dict[Type, Type]]

                                      i.e. for each "conditionally driven
                                      value", we store a mapping from a
                                      "condition" to a "conditional driver for
                                      that condition"

        `_when_conds`: List of when objects that have assignments handled by
                       this instance (added in definition_context.py indirectly
                       by a WhenCtx object when it is created)

        `_value_to_port_name_map`: Mapping from value to port name used by the
                                   backend during code generation to lookup the
                                   appropriate instance port for a given value
        """
        super().__init__("_magma_conditional_driver_" + str(id(context)))
        self._conditionally_driven_info = {}
        self._when_conds = []
        self._value_to_port_name_map = {}

    def add_when_cond(self, cond):
        self._when_conds.append(cond)

    @property
    def when_conds(self):
        return [x for x in self._when_conds if x.has_conditional_wires()]

    @property
    def conditional_values(self):
        return list(self._conditionally_driven_info.keys())

    def make_conditional_output(self, value):
        name = f"x{len(self._value_to_port_name_map)}"
        self._value_to_port_name_map[value] = name
        self._conditionally_driven_info[value] = {}
        self._add_port(name, Out(type(value)))
        return getattr(self, name)

    def remove(self, value):
        info = self._conditionally_driven_info[value]
        for when_tuple, driver in info.items():
            if when_tuple is None:
                continue
            # Remove tracking so we can avoid code generation if all
            # condintional wires are removed
            when_tuple[-1].remove_conditional_wire(value)
        del self._conditionally_driven_info[value]
        # Just leave ports for now, but we could remove them if we added
        # support to builder

    def _add_missing_conds(self, when_tuple, debug_info):
        """
        Add/wire port for a cond value if needed
        """
        for when in when_tuple:
            cond_value = when.cond
            if getattr(cond_value, 'is_otherwise_cond', False):
                # No condition, skip
                continue
            if cond_value in self._value_to_port_name_map:
                # Already added, skip
                continue

            cond_name = f"x{len(self._value_to_port_name_map)}"
            self._add_port(cond_name, In(type(cond_value)))
            getattr(self, cond_name).unconditional_wire(cond_value, debug_info)
            self._value_to_port_name_map[cond_value] = cond_name

    def add_conditional_driver(self, target, value, when_tuple, debug_info):
        """
        For the case when a driven value is conditionally driven in a
        subsequent when statement, e.g.

        x @= y  # default driver
        m.when(z):
            x @= w

        The special case condition `None` is used to identify the default
        driver in `self._conditionally_driven_info`
        """
        # Update info mapping, assumes `target` has already been added by
        # `make_conditional_output` which is called the first time a Wireable
        # is conditionally assigned (inside Wireable._conditional_wire)
        self._conditionally_driven_info[target][when_tuple] = value

        if when_tuple is not None:
            # Add ports for any conditions in cond tuple where each entry is a
            # when context
            self._add_missing_conds(when_tuple, debug_info)

        # Add port for the driving value if it does not exist
        if value not in self._value_to_port_name_map:
            value_name = f"x{len(self._value_to_port_name_map)}"
            self._add_port(value_name, In(type(value)))
            getattr(self, value_name).unconditional_wire(value, debug_info)
            self._value_to_port_name_map[value] = value_name

        if when_tuple is not None:
            # We track conditional wires added/removed from conditions so we
            # can skip code generation of empty when statements (e.g. if the
            # assignments are overridden at a later time)
            when_tuple[-1].add_conditional_wire(target, value, debug_info)

    def _finalize(self):
        """
        Store information used by the backend to recover original when
        statement structures, see __init__ for more information
        """
        self._dct['_is_conditional_driver_'] = True
        self._dct['conditional_values'] = self.conditional_values
        self._dct['conditionally_driven_info'] = self._conditionally_driven_info
        self._dct['value_to_port_name_map'] = self._value_to_port_name_map
        self._dct['when_conds'] = self.when_conds


def _make_conditional_driver(self):
    return ConditionalDriver(self)


DefinitionContext._make_conditional_driver = _make_conditional_driver
