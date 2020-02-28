from .passes import CircuitPass
from ..circuit import StagedCircuit


class FinalizeStagedCircuitPass(CircuitPass):
    def __call__(self, circuit):
        if issubclass(circuit, StagedCircuit):
            if not circuit.finalized:
                # TODO: Should we implicitly call open for them?
                circuit.finalize()
                circuit.finalized = True
