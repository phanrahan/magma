from abc import abstractmethod, ABC
from collections import namedtuple
from .simulator import CircuitSimulator
from .transforms import flatten, setup_clocks
from .circuit import *
from .scope import *
from .array import ArrayType
from .bit import VCC, GND

__all__ = ['PythonSimulator']

ExecutionOrder = namedtuple('ExecutionOrder', ['before', 'stateful', 'after'])

class SimPrimitive:
    def __init__(self, primitive, value_map):
        self.primitive = primitive
        self.inputs = []
        self.outputs = []
        self.value_map = value_map
        self.state_storage = {}

        for bit in self.primitive.interface.ports.values():
            if not isinstance(bit, ArrayType):
                bit = [bit]
            for b in bit:
                if b.isinput():
                    self.inputs.append(b)
                else:
                    self.outputs.append(b)

        self.set_constant_inputs()

    def stateful(self):
        return self.primitive.stateful

    def set_constant_inputs(self):
        for i in self.inputs:
            assert i.driven()
            o = i.value()
            if o.const():
                if o is VCC:
                    self.value_map[i] = True
                elif o is GND:
                    self.value_map[i] = False

    def inputs_satisfied(self):
        for i in self.inputs:
            if i not in self.value_map:
                return False

        return True

    def initialize_outputs(self):
        # Initializes all outputs to False, should perhaps
        # initialize based on starting inputs?
        for o in self.outputs:
            self.value_map[o] = False

    def propagate_outputs(self):
        for out in self.outputs:
            deps = out.dependencies()
            cur_val = self.value_map[out]
            for d in deps:
                self.value_map[d] = cur_val

    def simulate(self):
        self.primitive.simulate(self.value_map, self.state_storage)
        self.propagate_outputs()


class PythonSimulator(CircuitSimulator):
    def __setup_primitives(self):
        wrapped = []
        for primitive in self.circuit.instances:
            wrapped.append(SimPrimitive(primitive, self.value_map))

        return wrapped

    def __propagate_circuit_inputs(self):
        for bit in self.circuit_inputs:
            deps = bit.dependencies()
            cur_val = self.value_map[bit]
            for d in deps:
                self.value_map[d] = cur_val

    def __setup_circuit(self):
        self.clkbit = self.circuit.interface.ports['CLKIN']

        self.circuit_inputs = []
        self.circuit_outputs = []
        for name, bit in self.circuit.interface.ports.items():
            if not isinstance(bit, ArrayType):
                bit = [bit]
            for b in bit:
                if b.isoutput():
                    self.circuit_inputs.append(b)
                    self.value_map[b] = False
                else:
                    self.circuit_outputs.append(b)

        self.__propagate_circuit_inputs()

    def __outputs_initialized(self):
        for bit in self.circuit_outputs:
            if bit.isinput():
                if bit not in self.value_map:
                    return False

        return True

    def __get_ordered_primitives(self, unordered_primitives):
        before_state = []
        state_primitives = []
        after_state = []

        while True:
            found = False
            for primitive in unordered_primitives:
                if primitive.inputs_satisfied() and not primitive.stateful():
                    primitive.initialize_outputs()
                    primitive.propagate_outputs()
                    before_state.append(primitive)
                    unordered_primitives.remove(primitive)
                    found = True

            if not found:
                break

        state_primitives = []
        for primitive in unordered_primitives:
            if primitive.stateful():
                primitive.initialize_outputs()
                primitive.propagate_outputs()
                state_primitives.append(primitive)

        unordered_primitives[:] = [u for u in unordered_primitives if not u.stateful()]

        after_state = []
        while len(unordered_primitives) > 0:
            found = False
            for primitive in unordered_primitives:
                if primitive.inputs_satisfied():
                    primitive.initialize_outputs()
                    primitive.propagate_outputs()
                    after_state.append(primitive)
                    unordered_primitives.remove(primitive)
                    found = True
                    break
            assert found, "Some circuits have unsatisfied inputs"
        
        return ExecutionOrder(before=before_state, stateful=state_primitives, after=after_state)

    def __init__(self, main_circuit):
        setup_clocks(main_circuit)
        self.txfm = flatten(main_circuit)
        self.circuit = self.txfm.circuit
        self.value_map = {}
        self.__setup_circuit()

        primitives = self.__setup_primitives()

        self.execution_order = self.__get_ordered_primitives(primitives)

        assert self.__outputs_initialized(), "All circuit outputs not initialized."

    def get_capabilities(self):
        return []

    def get_value(self, bit, scope):
        newbit = self.txfm.get_new_bit(bit, scope)
        if isinstance(newbit, ArrayType):
            arr = [self.value_map.get(b) for b in newbit]
            for a in arr:
                if a is None:
                    return None

            return arr
        else:
            return self.value_map.get(newbit)

    def set_value(self, bit, scope, newval):
        newbit = self.txfm.get_new_bit(bit, scope)
        if newbit not in self.circuit_inputs:
            print("Only setting main's inputs is supported")
        else:
            self.value_map[newbit] = newval

    def evaluate(self):
        self.__propagate_circuit_inputs()

        for primitive in self.execution_order.before:
            primitive.simulate()
        for primitive in self.execution_order.stateful:
            primitive.simulate()
        for primitive in self.execution_order.after:
            primitive.simulate()

    def step(self):
        cur_clock_val = self.value_map[self.clkbit]
        self.value_map[self.clkbit] = not cur_clock_val
