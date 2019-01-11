from abc import ABC, abstractmethod
import tempfile
import uuid
from .compile import compile
import coreir
from .logging import warning


class CircuitDatabaseInterface(ABC):
    @abstractmethod
    def insert(self, circuit):
        pass

    @abstractmethod
    def clear(self):
        pass


class ConservativeCircuitDatabase(CircuitDatabaseInterface):
    def insert(self, circuit):
        name = circuit.name
        new_name = name + "-" + str(uuid.uuid4())
        type(circuit).rename(circuit, new_name)

    def clear(self):
        pass


class CircuitDatabase(CircuitDatabaseInterface):
    class Entry:
        def __init__(self, name):
            self.name = name
            self.circuits = {}

        def hash(self, circuit):
            with tempfile.TemporaryDirectory() as tempdir:
                try:
                    compile(tempdir + "/circuit", circuit, output="coreir", context=coreir.Context())
                    json_str = open(tempdir + "/circuit.json").read()
                except Exception as e:
                    warning(f"Could not compile circuit: '{str(e)}'. Uniquifying anyway.")
                    json_str = uuid.uuid4()
            return hash(json_str)

        def add_circuit(self, circuit):
            hash_ = self.hash(circuit)
            if hash_ in self.circuits:
                index = self.circuits[hash_][0]
            else:
                index = len(self.circuits)
                self.circuits[hash_] = (index, circuit)
            if index > 0:
                type(circuit).rename(circuit, circuit.name + "_unq" + str(index))

        def __repr__(self):
            return repr(self.circuits)

    def __init__(self):
        self.entries = {}

    def insert(self, circuit):
        name = circuit.name
        entry = self.entries.setdefault(name, CircuitDatabase.Entry(name))
        entry.add_circuit(circuit)

    def clear(self):
        self.entries = {}
