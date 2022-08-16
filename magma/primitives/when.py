import abc
import itertools
from typing import Dict, Iterable, Optional, Set, Tuple, Union

from magma.circuit import Circuit, CircuitType, CircuitBuilder
from magma.digital import Digital
from magma.t import Type
from magma.when import (
    BlockBase as WhenBlock,
    get_all_blocks as get_all_when_blocks,
    no_when,
)
from magma.wire import wire


_ISWHEN_KEY = "_iswhen_"


def iswhen(inst_or_defn: Union[Circuit, CircuitType]) -> bool:
    if isinstance(inst_or_defn, Circuit):
        return getattr(type(inst_or_defn), _ISWHEN_KEY, False)
    return getattr(inst_or_defn, _ISWHEN_KEY, False)


class WhenBuilder(CircuitBuilder):
    def __init__(self, block: WhenBlock):
        super().__init__(name=f"When_{id(block)}")
        self._block = block
        self._condition_counter = itertools.count()
        self._driver_counter = itertools.count()
        self._drivee_counter = itertools.count()
        self._input_counter = itertools.count()
        self._output_counter = itertools.count()
        self._input_to_index = {}
        self._output_to_index = {}
        self._default_drivers = {}
        self._set_definition_attr("primitive", True)
        self._set_definition_attr(_ISWHEN_KEY, True)
        self._set_definition_attr("_builder_", self)

    @property
    def default_drivers(self) -> Dict[Type, Type]:
        return self._default_drivers.copy()

    @property
    def input_to_index(self) -> Dict[Type, int]:
        return self._input_to_index.copy()

    @property
    def output_to_index(self) -> Dict[Type, int]:
        return self._output_to_index.copy()

    def _generic_add(
            self,
            value,
            value_to_index,
            index_counter,
            name_counter,
            name_prefix
    ):
        if value is None or value in value_to_index:
            return
        value_to_index[value] = next(index_counter)
        port_name = f"{name_prefix}{next(name_counter)}"
        self._add_port(port_name, type(value).flip())
        with no_when():
            wire(getattr(self, port_name), value)

    def add_drivee(self, value: Type):
        self._generic_add(
            value,
            self._output_to_index,
            self._output_counter,
            self._drivee_counter,
            "O"
        )

    def add_driver(self, value: Type):
        self._generic_add(
            value,
            self._input_to_index,
            self._input_counter,
            self._driver_counter,
            "I"
        )

    def add_condition(self, condition: Optional[Digital]):
        self._generic_add(
            condition,
            self._input_to_index,
            self._input_counter,
            self._condition_counter,
            "S"
        )

    def add_default_driver(self, drivee: Type, driver: Type):
        self.add_driver(driver)
        self.add_drivee(drivee)
        self._default_drivers[drivee] = driver

    def consume_block(self, block: WhenBlock):
        raise NotImplementedError()
        self.add_condition(block.condition)
        for conditional_wire in block.conditional_wires():
            self.add_drivee(conditional_wire.drivee)
            self.add_driver(conditional_wire.driver)
        for wire in block.default_drivers():
            self.add_default_driver(wire.drivee, wire.driver)

    @property
    def block(self) -> WhenBlock:
        return self._block
