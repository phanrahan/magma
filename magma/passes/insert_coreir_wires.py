from ..array import Array
from magma.bit import Bit
from ..bits import Bits
from ..circuit import coreir_port_mapping
from ..conversions import as_bits, from_bits
from ..digital import Digital
from ..generator import Generator2
from ..interface import IO
from .passes import DefinitionPass
from ..ref import NamedRef, ArrayRef, PortViewRef
from ..t import In, Out
from ..tuple import Tuple


def _sanitize_name(name):
    return name.replace("[", "_").replace("]", "")


def _simulate_wire(self, value_store, state_store):
    value_store.set_value(self.O, value_store.get_value(self.I))


class Wire(Generator2):
    def __init__(self, T):
        if issubclass(T, Digital):
            coreir_lib = "corebit"
            coreir_genargs = None
            # Convert to bit so we wrap named types like clock if necessary
            T = Bit
        else:
            width = T.flat_length()
            T = Bits[width]
            coreir_lib = "coreir"
            coreir_genargs = {"width": width}
        self.name = "Wire"
        self.io = IO(I=In(T), O=Out(T))
        self.simulate = _simulate_wire
        self.coreir_name = "wire"
        self.coreir_lib = coreir_lib
        self.coreir_genargs = coreir_genargs
        self.renamed_ports = coreir_port_mapping


class InsertCoreIRWires(DefinitionPass):
    def __init__(self, main):
        super().__init__(main)
        self.seen = set()
        self.wire_map = {}

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
            with definition.open():
                wire_inst = Wire(T)(name=name)
                self.wire_map[driver] = wire_inst
        wire_inst = self.wire_map[driver]
        wire_input = wire_inst.I
        wire_output = wire_inst.O

        if is_bits:
            # Select the index off the parent bits wire
            wire_input = wire_input[index]
            wire_output = wire_output[index]
            driver = driver[index]

        if not isinstance(driver, Digital):
            driver = as_bits(driver)
            wire_output = from_bits(T, wire_output)

        # Could be already wired for fanout cases
        if not wire_input.driven():
            if isinstance(wire_input, Array):
                for d, w in zip(driver, wire_input):
                    # Could have wired up child elements already
                    if not w.driven():
                        w @= d
            else:
                wire_input @= driver
        value @= wire_output

    def _insert_wire(self, value, definition):
        if value.is_mixed():  # mixed children
            for child in value:
                if not child.is_output():
                    self._insert_wire(child, definition)
            return
        if value in self.seen:
            return  # in the case of inouts, we may see more than once
        self.seen.add(value)
        if not value.driven():
            return  # undriven value, skip wire insertion
        driver = value.value()

        while (driver is not None and driver.name.anon() and
               not driver.is_output()):
            value, driver = driver, driver.value()

        descend = (isinstance(driver, (Array, Tuple)) and
                   not driver.iswhole())
        if descend:
            for child in value:
                self._insert_wire(child, definition)
            return

        if driver is None or driver.is_output() or driver.is_inout():
            return

        if isinstance(driver.name, PortViewRef):
            # Don't descend into hierarchical connections since we assume this
            # logic will be run in that context in another stage of the pass
            return

        value.unwire(driver)
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
        for value in definition.interface.ports.values():
            if not value.is_output():
                self._insert_wire(value, definition)
