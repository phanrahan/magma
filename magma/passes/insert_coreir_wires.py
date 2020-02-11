from .passes import DefinitionPass
from ..digital import Digital
from ..generator import Generator
from ..circuit import Circuit, DeclareCoreirCircuit
from ..t import In, Out
from ..bits import Bits


def simulate_wire(self, value_store, state_store):
    value_store.set_value(self.O, value_store.get_value(self.I))


class Wire(Generator):
    @staticmethod
    def generate(name, T):
        if issubclass(T, Digital):
            width = 1
        else:
            width = T.flat_length()

        CoreIRWire = DeclareCoreirCircuit(
            "Wire",
            'I', In(Bits[width]), 'O', Out(Bits[width]),
            simulate=simulate_wire,
            coreir_name="wire",
            coreir_lib="coreir",
            coreir_genargs={"width": width}
        )

        class WrappedWire(Circuit):
            IO = ["I", In(T), "O", Out(T)]

            @classmethod
            def definition(circuit):
                wire_inst = CoreIRWire(name=name)
                wire_inst.I @= circuit.I.as_bits()
                circuit.O @= T.from_bits(wire_inst.O)
        return WrappedWire


class InsertCoreIRWires(DefinitionPass):
    def insert_wire(self, value, definition):
        driver = value.value()
        while driver is not None and driver.name.anon():
            driver = driver.value()
        if driver is not None:
            value.unwire(driver)
            name = f"wire_{driver.name}_{value.name}"
            wire_inst = definition.add_instance(
                Wire, name, type(value), name=name
            )
            wire_inst.I @= driver
            value @= wire_inst.O
            if not driver.is_output():
                self.insert_wire(driver, definition)

    def __call__(self, definition):
        for instance in definition.instances:
            for name, value in instance.ports.items():
                if value.is_input():
                    print(name, value, value.value())
        for value in definition.interface.ports.values():
            if value.is_input():
                self.insert_wire(value, definition)
