from .passes import DefinitionPass
from ..digital import Digital
from ..generator import Generator
from ..circuit import Circuit, DeclareCoreirCircuit
from ..t import In, Out
from ..digital import Digital
from ..array import Array
from ..tuple import Tuple
from ..bits import Bits
from ..ref import NamedRef


def _simulate_wire(self, value_store, state_store):
    value_store.set_value(self.O, value_store.get_value(self.I))


class Wire(Generator):
    @staticmethod
    def generate(T):
        if issubclass(T, Digital):
            coreir_lib = "corebit"
            coreir_genargs = None
        else:
            coreir_lib = "coreir"
            width = T.flat_length()
            T = Bits[width]
            coreir_genargs = {"width": width}
        return DeclareCoreirCircuit(
            "Wire", 'I', In(T), 'O', Out(T),
            simulate=_simulate_wire,
            coreir_name="wire",
            coreir_lib=coreir_lib,
            coreir_genargs=coreir_genargs
        )


def _sanitize_name(name):
    return name.replace("[", "_").replace("]", "")


class InsertCoreIRWires(DefinitionPass):
    def __init__(self, main):
        super().__init__(main)
        self.seen = set()
        self.wire_map = {}

    def insert_wire(self, value, definition):
        if value.is_mixed():
            # mixed children
            for child in value:
                if not child.is_output():
                    self.insert_wire(child, definition)
            return
        if value in self.seen:
            # In the case of inouts, we may see more than once
            return
        self.seen.add(value)
        driver = value.value()

        while driver is not None and driver.name.anon():
            if isinstance(driver, (Array, Tuple)) and \
                    not driver.iswhole(driver.ts):
                for child in value:
                    self.insert_wire(child, definition)
                return
            driver = driver.value()
        if driver is None or driver.is_output() or driver.is_inout():
            return

        value.unwire(driver)
        T = type(driver)
        if driver not in self.wire_map:
            driver_name = driver.name.qualifiedname("_")
            value_name = value.name.qualifiedname("_")
            driver_name = _sanitize_name(driver_name)
            value_name = _sanitize_name(value_name)

            # Rename driver so it doesn't conflict with new wire instance name
            if isinstance(driver.name, NamedRef):
                driver.name.name = "_" + driver.name.name
            name = f"{driver_name}"
            with definition.open():
                wire_inst = Wire(T, name=name)
                self.wire_map[driver] = wire_inst
                if issubclass(T, Digital):
                    wire_inst.I @= driver
                else:
                    wire_inst.I @= driver.as_bits()
        else:
            wire_inst = self.wire_map[driver]

        if issubclass(T, Digital):
            value @= wire_inst.O
        else:
            value @= T.from_bits(wire_inst.O)

        self.insert_wire(driver, definition)

    def __call__(self, definition):
        # Copy instances because inserting wire will append to instances
        instances_copy = definition.instances.copy()
        for instance in instances_copy:
            for value in instance.interface.ports.values():
                if not value.is_output():
                    self.insert_wire(value, definition)
        for value in definition.interface.ports.values():
            if not value.is_output():
                self.insert_wire(value, definition)
