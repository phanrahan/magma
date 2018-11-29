from abc import ABC, abstractmethod
import tempfile
import uuid


class CircuitDatabaseEntry:
    def __init__(self, circuit, hash_, unique_name):
        self.circuit = circuit
        self.hash_ = hash_
        self.unique_name = unique_name


class CircuitDatabaseInterface(ABC):
    @abstractmethod
    def insert(self, circuit):
        pass


class ConservativeCircuitDatabase(CircuitDatabaseInterface):
    def insert(self, circuit):
        name = circuit.name
        new_name = name + "-" + str(uuid.uuid4())
        type(circuit).rename(circuit, new_name)


class CircuitDatabase(CircuitDatabaseInterface):
    class Entry:
        def __init__(self, name):
            self.name = name
            self.circuits = {}

        def hash(self, circuit):
            from .compile import compile
            import coreir
            with tempfile.TemporaryDirectory() as tempdir:
                compile(tempdir + "/circuit", circuit, output="coreir", context=coreir.Context())
                print (open(tempdir + "/circuit.json").read())
            return str(uuid.uuid4())

        def add_circuit(self, circuit):
            hash_ = self.hash(circuit)
            if hash_ in self.circuits:
                # TODO(rsetaluri): Do some rename.
                raise NotImplementedError()
                return
            type(circuit).rename(circuit, circuit.name + "-" + hash_)
            self.circuits[hash_] = circuit

        def __repr__(self):
            return repr(self.circuits)

    def __init__(self):
        self.entries = {}

    def insert(self, circuit):
        name = circuit.name
        entry = self.entries.setdefault(name, CircuitDatabase.Entry(name))
        entry.add_circuit(circuit)
