from magma.array import Array
from magma.bits import Bits
from magma.digital import Digital
from magma.clock import AsyncReset, AsyncResetN, Clock, _ClockType
from magma.conversions import as_bits, from_bits, bit, convertbit, convertbits
from magma.debug import maybe_get_debug_info
from magma.digital import Digital
from magma.generator import Generator2
from magma.passes.passes import DefinitionPass, pass_lambda
from magma.primitives.wire import Wire
from magma.ref import NamedRef, ArrayRef, PortViewRef, InstRef
from magma.t import In, Out
from magma.tuple import Tuple


def _sanitize_name(name):
    return name.replace("[", "_").replace("]", "")\
               .replace("(", "").replace(")", "")\
               .replace(",", "").replace(" ", "_")


class InsertCoreIRWires(DefinitionPass):
    def __init__(self, main, flatten: bool = True):
        super().__init__(main)
        self.seen = set()
        self.wire_map = {}
        self._flatten = flatten

    def _make_wire(self, driver, value, definition):
        is_bits = (isinstance(driver.name, ArrayRef) and
                   isinstance(driver, Digital) and not driver.name.anon())

        # If this is a member of a bits, emit only one wire for the parent
        # Bits, since it shouldn't be flattened
        if is_bits:
            index = driver.name.index
            driver = driver.name.array

        T = type(driver)
        if driver not in self.wire_map:
            driver_name = driver.name.qualifiedname("_")
            driver_name = _sanitize_name(driver_name)

            # Rename driver so it doesn't conflict with new wire instance name
            if isinstance(driver.name, NamedRef):
                driver.name.name = "_" + driver.name.name

            name = f"{driver_name}"
            wire_inst = Wire(T, flatten=self._flatten)(name=name)
            wire_inst.debug_info = maybe_get_debug_info(value)
            self.wire_map[driver] = wire_inst
        wire_inst = self.wire_map[driver]
        wire_input = wire_inst.I
        wire_output = wire_inst.O

        if is_bits:
            # Select the index off the parent bits wire
            wire_output = wire_output[index]
            # NOTE(leonardt): We don't select off the input and instead wire up
            # the entire bits (this avoids an "undriven" error when only one
            # index of the bits is used)

        if self._flatten and not is_bits and not isinstance(driver, Digital):
            driver = as_bits(driver)
            wire_output = from_bits(T, wire_output)

        # Could be already wired for fanout cases
        if not wire_input.driven():
            wire_input @= driver

        value_T = type(value)
        if not isinstance(wire_output, value_T):
            # This mean it was cast by the user (e.g. m.clock(value)), so we
            # need to "recast" the wire output
            if isinstance(value, Digital):
                wire_output = convertbit(wire_output, value_T)
            elif isinstance(value, Array):
                wire_output = convertbits(
                    wire_output, len(value_T), value_T,
                    issubclass(value_T, Bits)
                )
        value @= wire_output

    def _insert_wire(self, value, definition):
        if value.is_mixed():  # mixed children
            for child, _ in value.connection_iter():
                if not child.is_output():
                    self._insert_wire(child, definition)
            return
        if value in self.seen:
            return  # in the case of inouts, we may see more than once
        self.seen.add(value)
        if not value.driven():
            return  # undriven value, skip wire insertion
        driver = value.value()

        while driver is not None and driver.is_driven_anon_temporary():
            value, driver = driver, driver.value()

        descend = (isinstance(driver, (Array, Tuple)) and
                   driver.anon())
        if descend:
            for child, _ in value.connection_iter():
                self._insert_wire(child, definition)
            return

        if (driver is None or driver.is_output() or driver.is_inout() or
                driver.name.anon()):
            return

        if isinstance(driver.name.root(), InstRef):
            return

        if isinstance(driver.name, PortViewRef):
            # Don't descend into hierarchical connections since we assume this
            # logic will be run in that context in another stage of the pass
            return

        value.unwire(driver, keep_wired_when_contexts=True)
        with definition.open():
            self._make_wire(driver, value, definition)
            self._insert_wire(driver, definition)

    def __call__(self, definition):
        if getattr(definition, "_coreir_wires_inserted_", False):
            return
        definition._coreir_wires_inserted_ = True
        # Copy instances because inserting wire will append to instances.
        instances_copy = definition.instances.copy()
        for instance in instances_copy:
            for value in instance.interface.ports.values():
                if not value.is_output():
                    self._insert_wire(value, definition)

        # See https://github.com/phanrahan/magma/pull/1157 for more context, we
        # need to run this on specifically the when builder instance, since
        # this hasn't been finalized yet and may trace back to temporary
        # values.
        for builder in definition._context_._builders:
            if builder._finalized:
                continue
            for value in builder._io.inst_ports.values():
                if not value.is_output():
                    self._insert_wire(value, definition)
        for value in definition.interface.ports.values():
            if not value.is_output():
                self._insert_wire(value, definition)


insert_coreir_wires = pass_lambda(InsertCoreIRWires)
