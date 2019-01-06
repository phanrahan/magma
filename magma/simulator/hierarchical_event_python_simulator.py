import sys
from abc import abstractmethod
from collections import namedtuple
from simulator import CircuitSimulator

ExecutionState = namedtuple('ExecutionState', ['cycles', 'clock', 'triggered_points'])

class ExecutionList:
    pass

class SimCall:
    def __init__(self, instance, outputs):
        self.instance = instance
        self.outputs = outputs

class SimInfo:
    def get_stateful_instances(self):
        insts = []
        for inst in self.circuit.instances:
            siminfo = type(inst).siminfo
            if siminfo.is_stateful:
                insts.append(inst)

        return insts

    def deanonymize(self, wire):
        if isinstance(wire.name, AnonRef):
            wires = []

            assert(isinstance(wire, ArrayType) or isinstance(wire, TupleType))

            for elem in wire:
                wires += self.deanonymize(elem)

            return wires
        else:
            return [wire]

    def get_inst_and_circuit(self, wire):
        if isinstance(wire.name, DefnRef):
            return None, None

        indices = []
        while not isinstance(wire.name, InstRef):
            indices.append(wire.name.index)
            if isinstance(wire.name, ArrayRef):
                wire = wire.name.array
            elif isinstance(wire.name, TupleRef):
                wire = wire.name.tuple
            else:
                assert(False)

        inst = wire.name.inst
        circuit = type(inst)
        circuit_wire = circuit.interface.ports[wire.name]
        for idx in reversed(indices):
            circuit_wire = circuit_wire[idx]

        return inst, circuit_wire

    def get_all_bits(self, val):

        if isinstance(val, ArrayType) or isinstance(val, TupleType):
            bits = []

            for elem in val:
                bits += self.get_all_bits(elem)

            return bits
        elif isinstance(val, BitType):
            return [val]

    def get_required_inputs(self, output):
        # Output is the definition output
        required_inputs = set()
        for bit in self.get_all_bits(output):
            required_inputs |= self.required_inputs[bit]

        return required_inputs


    def analyze_state_dependencies(self, circuit):
        state_outputs = []
        for inst in self.stateful_instances:
            siminfo = type(inst).siminfo
            for out in inst.get_state_outputs():
                state_outputs.append(out)

    def compute_dependencies(self, wires):
        frontier = set(wires)
        required_inputs  = []
        while len(frontier) > 0:
            old_frontier = frontier
            frontier = set()

            for wire in old_frontier:
                for driver in self.deanonymize(wire.value()):
                    if driver.const():
                        continue

                    inst, circuit_output = self.get_inst_and_circuit(driver)
                    if inst is None: # Attached to definition
                        required_inputs.append(driver)

                    inst_info = type(inst).siminfo
                    for new_input in inst_info.get_required_inputs(circuit_output):
                        frontier.add(new_inputs)

    def compute_required_inputs(self):
        self.required_inputs = {}
        self.execution_lists = {}

        for output in self.circuit.interface.inputs():
            for wire in self.get_all_bits(output):
                inputs, execution_list = self.compute_dependencies([wire])
                self.required_inputs[wire] = inputs
                self.execution_lists[wire] = execution_list

    def __init__(self, circuit):
        self.circuit = circuit
        self.stateful_instances = self.get_stateful_instances()
        self.is_stateful = len(self.stateful_instances) > 0
        self.compute_required_inputs()

        self.state_dependencies = self.analyze_state_dependencies()

class ValueStore:
    def __init__(self):
        self.value_map = {}

    def set_value(self, scope, bit, val):
        pass

    def get_value(self, scope, bit):
        pass

class HierarchicalEventPythonSimulator(CircuitSimulator):
    def __init__(self, circuit, clock):
        self.value_store = ValueStore()
        self.queue = []

    def get_capabilities(self):
        return []

    def get_value(self, bit, scope):
        pass

    def set_value(self, bit, scope, newval):
        pass

    def advance(self, halfcycles):
        pass

    def evaluate(self_):
        pass

    def rewind(self, halfcycles):
        pass

    def cont(self):
        pass

    def add_watchpoint(self, bit, scope, value=None):
        pass

    def delete_watchpoint(self, num):
        pass
