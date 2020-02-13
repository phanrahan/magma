from .passes import DefinitionPass
from ..digital import Digital
from ..generator import Generator
from ..circuit import Circuit, DeclareCoreirCircuit
from ..t import In, Out
from ..array import Array
from ..tuple import Tuple
from ..bits import Bits


def simulate_wire(self, value_store, state_store):
    value_store.set_value(self.O, value_store.get_value(self.I))


class Wire(Generator):
    @staticmethod
    def generate(width):
        return DeclareCoreirCircuit(
            "Wire",
            'I', In(Bits[width]), 'O', Out(Bits[width]),
            simulate=simulate_wire,
            coreir_name="wire",
            coreir_lib="coreir",
            coreir_genargs={"width": width}
        )


class InsertCoreIRWires(DefinitionPass):
    def __init__(self, main):
        super().__init__(main)
        self.seen = set()

    def _sanitize_name(self, name):
        return name.replace("[", "_").replace("]", "")

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
            driver = driver.value()
        if driver is not None and not driver.is_output():
            value.unwire(driver)

            driver_name = driver.name.qualifiedname("_")
            value_name = value.name.qualifiedname("_")
            driver_name = self._sanitize_name(driver_name)
            value_name = self._sanitize_name(value_name)

            name = f"wire_{driver_name}_{value_name}"
            T = type(driver)
            wire_inst = definition.add_instance(
                Wire, T.flat_length(), name=name
            )
            wire_inst.I @= driver.as_bits()
            value @= T.from_bits(wire_inst.O)

            if not driver.is_output():
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
