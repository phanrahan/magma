from abc import ABC, abstractmethod
import tempfile
import uuid
from .compile import compile
import coreir
from .logging import warning
from .config import get_database_hash_backend
from magma.backend.coreir_ import CoreIRBackend


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
                    backend = get_database_hash_backend()
                    if backend == "coreir":
                        if hasattr(circuit, "wrappedModule") and circuit.wrappedModule:
                            circuit.wrappedModule.save_to_file(tempdir + "/circuit.json")
                        else:
                            compile(tempdir + "/circuit", circuit, output="coreir")
                        # Mark graph as dirty so future JSON passes will run,
                        # otherwise it will not register our changes via the
                        # API
                        CoreIRBackend().context.run_passes(["markdirty"])
                        string = open(tempdir + "/circuit.json").read()
                    elif backend == "verilog":
                        compile(tempdir + "/circuit", circuit, backend)
                        string = open(tempdir + "/circuit.v").read()
                    else:
                        raise NotImplementedError(backend)
                except Exception as e:
                    warning(f"Could not compile circuit {circuit}: '{str(e)}'. Uniquifying anyway.")
                    raise e
                    string = uuid.uuid4()
            return hash(string)

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
