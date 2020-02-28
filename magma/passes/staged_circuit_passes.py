from .passes import CircuitPass
from ..circuit import StagedCircuit


class FinalizeStagedCircuitPass(CircuitPass):
    def __call__(self, circuit):
        if issubclass(circuit, StagedCircuit):
            # TODO: Should we implicitly call open for them?
            circuit.finalize()
