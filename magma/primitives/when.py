import functools
import itertools
from typing import Dict, Optional, Union, Set

from magma.bits import Bits
from magma.circuit import Circuit, CircuitType, CircuitBuilder
from magma.clock import Enable
from magma.conversions import from_bits
from magma.digital import Digital
from magma.primitives.register import AbstractRegister
from magma.ref import DerivedRef
from magma.t import Type, In, Out
from magma.when import (
    BlockBase as WhenBlock,
    no_when,
    find_inferred_latches,
)
from magma.value_utils import make_selector
from magma.wire import wire


_ISWHEN_KEY = "_iswhen_"


def iswhen(inst_or_defn: Union[Circuit, CircuitType]) -> bool:
    if isinstance(inst_or_defn, Circuit):
        return getattr(type(inst_or_defn), _ISWHEN_KEY, False)
    return getattr(inst_or_defn, _ISWHEN_KEY, False)


class InferredLatchError(Exception):
    pass


# NOTE(rsetaluri): This is needed because importing magma.primitives.Memory
# results in a circular import.
@functools.lru_cache(maxsize=1)
def _Memory():
    from magma.primitives.memory import Memory
    return Memory


def _is_memory_port(value: Type) -> bool:
    Memory = _Memory()
    root_ref = value.name.root()
    try:
        value_inst = root_ref.inst
    except AttributeError:
        return False
    if not isinstance(type(value_inst), Memory):
        return False
    if root_ref.name not in ("WDATA", "WADDR", "WE", "RADDR"):
        return False
    return True


def _add_default_drivers_to_memory_ports(
    builder: 'WhenBuilder', latches: Set[Type]
):
    # TODO(leonardt): for waddr/wdata/raddr, we could use an existing value as a
    # default since ren/wen will be low, this would avoid potentially adding an
    # extra input to the select mux
    for drivee in builder.output_to_index:
        if drivee in builder.default_drivers:
            continue
        if not _is_memory_port(drivee):
            continue
        if drivee not in latches:
            continue
        T = type(drivee).undirected_t
        zero = from_bits(T, Bits[T.flat_length()](0))
        builder.block.add_default_driver(drivee, zero)
        latches.remove(drivee)


def _get_corresponding_register_default(value: Type) -> Optional[Type]:
    """Used to get the corresponding default for `value` if it is a
    reference to a register input value.

    `value` should either be reg.I or reg.CE:
        * For reg.I, the default will be reg.O (default update is the
          current value).
        * For reg.CE, the default will be False (default to no update).

    """
    root_ref = value.name.root()
    try:
        value_inst = root_ref.inst
    except AttributeError:
        return None
    value_inst_T = type(value_inst)
    if not isinstance(value_inst_T, AbstractRegister):
        return None
    if value is value_inst_T.get_enable(value_inst):
        return type(value)(False)
    sel = make_selector(value)
    return sel.select(value_inst.O)


def _add_default_drivers_to_register_inputs(
    builder: 'WhenBuilder', latches: Set[Type]
):
    """Adds default drivers to register inputs (reg.O is the default value for
    inputs, False is the default for enables).

    The current implementation assumes the magma internally defined register
    primitive is used, which always has only one input and an optional enable
    port. If we encounter a AbstractRegister, we will drive all inputs with
    reg.O and all enables with reg.I (if they have multiple).

    If we wanted to make this interface more extensible, we could have the user
    provide an API for setting up default values.
    """
    for drivee in builder.output_to_index:
        if drivee not in latches:
            continue
        O = _get_corresponding_register_default(drivee)
        if O is None:
            continue
        builder.block.add_default_driver(drivee, O)
        latches.remove(drivee)


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
        self._input_to_name = {}
        self._output_to_name = {}
        self._default_drivers = {}
        self._set_definition_attr("primitive", True)
        self._set_definition_attr(_ISWHEN_KEY, True)
        self._set_definition_attr("_builder_", self)
        self._is_when_builder_ = True

    @property
    def default_drivers(self) -> Dict[Type, Type]:
        return self._default_drivers.copy()

    @property
    def input_to_index(self) -> Dict[Type, int]:
        return self._input_to_index.copy()

    @property
    def output_to_index(self) -> Dict[Type, int]:
        return self._output_to_index.copy()

    def _check_existing_derived_ref(self, value, value_to_name, value_to_index):
        """If value is a child of an array or tuple that has already been added,
        we return the child of the existing value, rather than adding a new
        port, which allows us to maintain bulk assignments in the eventual
        generated if statement, rather that elaborating into per-child
        assignments.
        """
        curr_root = None
        for ref in value.name.root_iter(
            stop_if=lambda ref: not isinstance(ref, DerivedRef)
        ):
            if ref.parent_value in value_to_index:
                curr_root = ref.parent_value
        if not curr_root:
            return
        root_port = getattr(self, value_to_name[curr_root])
        return make_selector(value, stop_at=curr_root).select(root_port)

    def _generic_add(
            self,
            value,
            value_to_index,
            index_counter,
            name_counter,
            value_to_name,
            name_prefix,
            type_qualifier,
    ):
        if value in value_to_index:
            return
        value_to_index[value] = next(index_counter)
        port_name = f"{name_prefix}{next(name_counter)}"
        value_to_name[value] = port_name

        port = self._check_existing_derived_ref(value, value_to_name,
                                                value_to_index)
        # NOTE(leonardt): when we add support for flatten_all_tuples=False, we
        # should also add similar logic here to avoid flattening assignments
        if port is None:
            self._add_port(port_name, type_qualifier(type(value).undirected_t))
            port = getattr(self, port_name)
            port.is_when_port = True

        with no_when():
            if value.is_input() and isinstance(value, Enable):
                value.wire(
                    port,
                    driven_implicitly_by_when=value.driven_implicitly_by_when
                )
            elif port.is_input() and port.driven():
                port.rewire(value)
            else:
                wire(port, value)
                port.debug_info = self.debug_info
                value.debug_info = self.debug_info

    def add_drivee(self, value: Type):
        self._generic_add(
            value,
            self._output_to_index,
            self._output_counter,
            self._drivee_counter,
            self._output_to_name,
            "O",
            Out,
        )

    def add_driver(self, value: Type):
        self._generic_add(
            value,
            self._input_to_index,
            self._input_counter,
            self._driver_counter,
            self._input_to_name,
            "I",
            In,
        )

    def add_condition(self, condition: Optional[Digital]):
        self._generic_add(
            condition,
            self._input_to_index,
            self._input_counter,
            self._condition_counter,
            self._input_to_name,
            "S",
            In,
        )

    def add_default_driver(self, drivee: Type, driver: Type):
        self.add_driver(driver)
        self.add_drivee(drivee)
        self._default_drivers[drivee] = driver

    def remove_default_driver(self, drivee: Type):
        del self._default_drivers[drivee]

    def _finalize(self):
        # Detect latches which would be inferred from the context of the when
        # block.
        latches = find_inferred_latches(self.block)
        # NOTE(rsetaluri): These passes should ideally be done after circuit
        # creation. However, it is quite unwieldy, so we opt to do it in this
        # builder's finalization, although it is a bit "hacky". Ideally, this
        # builder should be completely agnostic of anything it is connected to,
        # and a global (post-processing) pass should be used instead.
        # NOTE(leonardt): We only add default drivers if a value is inferred to
        # be a latch, otherwise we skip this implicit logic so the output is
        # cleaner (e.g. if a register is assigned in every case, we don't need
        # the default value).
        _add_default_drivers_to_memory_ports(self, latches)
        _add_default_drivers_to_register_inputs(self, latches)

        if latches:
            raise InferredLatchError(latches)

    @property
    def block(self) -> WhenBlock:
        return self._block


def is_when_builder(builder):
    return isinstance(builder, WhenBuilder)
