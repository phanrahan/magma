from ..array import Array
from ..bits import Bits
from ..circuit import coreir_port_mapping
from ..conversions import as_bits, from_bits
from ..digital import Digital
from ..generator import Generator2
from ..interface import IO
from .passes import DefinitionPass
from ..ref import NamedRef
from ..t import In, Out
from ..tuple import Tuple


def _simulate_wire(self, value_store, state_store):
    value_store.set_value(self.O, value_store.get_value(self.I))


def _sanitize_name(name):
    return name.replace("[", "_").replace("]", "")


class _Wire(Generator2):
    def __init__(self, T):
        if issubclass(T, Digital):
            coreir_lib = "corebit"
            coreir_genargs = None
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

    def get_wire(self, driver, value, definition):
        root = driver.name.root()
        if root is None:
            root = driver
        T = type(root)
        if root not in self.wire_map:

            root_name = root.name.qualifiedname("_")
            root_name = _sanitize_name(root_name)

            # Rename root so it doesn't conflict with new wire instance name
            assert isinstance(root.name, NamedRef)
            root.name.name = "_" + root.name.name

            name = f"{root_name}"
            with definition.open():
                wire_inst = _Wire(T)(name=name)
                self.wire_map[root] = wire_inst
        wire_inst = self.wire_map[root]
        wire_input = wire_inst.I
        wire_output = wire_inst.O
        if not issubclass(T, Digital):
            wire_input = from_bits(T, wire_input)
            wire_output = from_bits(T, wire_output)
        return wire_input, wire_output

    def insert_wire(self, value, definition):
        if value.is_mixed():  # mixed children
            for child in value:
                if not child.is_output():
                    self.insert_wire(child, definition)
            return
        if value in self.seen:
            return  # in the case of inouts, we may see more than once
        self.seen.add(value)
        driver = value.value()

        while (driver is not None and driver.name.anon() and
               not driver.is_output()):
            descend = (isinstance(driver, (Array, Tuple)) and
                       not driver.iswhole())
            if descend:
                for child in value:
                    self.insert_wire(child, definition)
                return
            driver = driver.value()
        if driver is None or driver.is_output() or driver.is_inout():
            return

        value.unwire(driver)
        T = type(driver)
        wire_input, wire_output = self.get_wire(driver, value, definition)

        if driver.name.root() is not None and driver.name.root() is not driver:
            wire_input = driver.name.get_from_root(wire_input)
            wire_output = driver.name.get_from_root(wire_output)

        wire_input @= driver
        value @= wire_output

        self.insert_wire(driver, definition)

    def __call__(self, definition):
        # Copy instances because inserting wire will append to instances.
        instances_copy = definition.instances.copy()
        for instance in instances_copy:
            for value in instance.interface.ports.values():
                if not value.is_output():
                    self.insert_wire(value, definition)
        for value in definition.interface.ports.values():
            if not value.is_output():
                self.insert_wire(value, definition)
