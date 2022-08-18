import abc
import itertools
from typing import Dict, Iterable, Optional, Set, Tuple, Union

from magma.bits import Bits
from magma.circuit import Circuit, CircuitType, CircuitBuilder
from magma.conversions import from_bits
from magma.digital import Digital
from magma.t import Type, In, Out
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


def _get_memory_port(value: Type) -> Optional[Type]:
    # NOTE(rsetaluri): Memory results in a circular import.
    from magma.primitives.memory import Memory
    root_ref = value.name.root()
    try:
        value_inst = root_ref.inst
    except AttributeError:
        return None
    if not isinstance(type(value_inst), Memory):
        return None
    if root_ref.name not in ("WDATA", "WADDR", "WE", "RADDR"):
        return None
    return value


def _add_default_drivers_to_memory_ports(builder: 'WhenBuilder'):
    for port in builder.output_to_index:
        port = _get_memory_port(port)
        if port is None:
            continue
        T = type(port).undirected_t
        zero = from_bits(T, Bits[T.flat_length()](0))
        builder.block.add_default_driver(port, zero)


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
            name_prefix,
            type_qualifier,
    ):
        if value is None or value in value_to_index:
            return
        value_to_index[value] = next(index_counter)
        port_name = f"{name_prefix}{next(name_counter)}"
        self._add_port(port_name, type_qualifier(type(value).undirected_t))
        with no_when():
            wire(getattr(self, port_name), value)

    def add_drivee(self, value: Type):
        self._generic_add(
            value,
            self._output_to_index,
            self._output_counter,
            self._drivee_counter,
            "O",
            Out,
        )

    def add_driver(self, value: Type):
        self._generic_add(
            value,
            self._input_to_index,
            self._input_counter,
            self._driver_counter,
            "I",
            In,
        )

    def add_condition(self, condition: Optional[Digital]):
        self._generic_add(
            condition,
            self._input_to_index,
            self._input_counter,
            self._condition_counter,
            "S",
            In,
        )

    def add_default_driver(self, drivee: Type, driver: Type):
        self.add_driver(driver)
        self.add_drivee(drivee)
        self._default_drivers[drivee] = driver

    def _finalize(self):
        # NOTE(rsetaluri): This should ideally be done in a pass after circuit
        # creation. However, it is quite unwieldy, so we opt to do it in this
        # builder's finalization, although it is a bit "hacky". Ideally, this
        # builder should be completely agnostic of anything it is connected to,
        # and a global (post-processing) pass should be used instead.
        _add_default_drivers_to_memory_ports(self)

    @property
    def block(self) -> WhenBlock:
        return self._block