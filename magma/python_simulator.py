import sys
from abc import abstractmethod
if sys.version_info < (3, 4):
    import abc
    ABC = abc.ABCMeta('ABC', (object,), {})
else:
    from abc import ABC
from collections import namedtuple
from .simulator import CircuitSimulator, ExecutionState
from .transforms import flatten, setup_clocks
from .circuit import *
from .scope import *
from .array import ArrayType
from .bit import VCC, GND, BitType

__all__ = ['PythonSimulator']

ExecutionOrder = namedtuple('ExecutionOrder', ['stateful', 'combinational'])


class PythonSimulatorException(Exception):
    pass


class SimPrimitive:
    def __init__(self, primitive, value_store):
        if primitive.simulate is None:
            raise ValueError("Cannot simulate {} of type {} because it does not have a Python simulate method".format(primitive, type(primitive)))
        self.primitive = primitive
        self.inputs = []
        self.outputs = []
        self.value_store = value_store
        self.state_store = {}

        for bit in self.primitive.interface.ports.values():
            if not isinstance(bit, ArrayType):
                bit = [bit]
            for b in bit:
                if b.isinput():
                    self.inputs.append(b)
                else:
                    self.outputs.append(b)

    def stateful(self):
        return self.primitive.stateful

    def inputs_satisfied(self):
        for i in self.inputs:
            if not self.value_store.value_initialized(i):
                return False

        return True

    def initialize_outputs(self):
        # Initializes all outputs to False, should perhaps
        # initialize based on starting inputs?
        for o in self.outputs:
            self.value_store.set_value(o, False)

    def simulate(self):
        self.primitive.simulate(self.value_store, self.state_store)

class WatchPoint:
    idx = 0
    def __init__(self, bit, scope, simulator, value):
        self.bit = bit
        self.scope = scope
        self.simulator = simulator
        self.value = value
        self.old_val = self.simulator.get_value(self.bit, self.scope)

        WatchPoint.idx += 1
        self.idx = WatchPoint.idx

    def was_triggered(self):
        new_val = self.simulator.get_value(self.bit, self.scope)
        triggered = new_val != self.old_val 
        if self.value:
            if self.value != new_val:
                triggered = False
        self.old_val = new_val

        return triggered

class ValueStore:
    def __init__(self):
        self.value_map = {}

    def value_initialized(self, bit):
        if isinstance(bit, ArrayType):
            for b in bit:
                if not self.value_initialized(b):
                    return False

            return True

        if bit.isinput():
            bit = bit.value()

        if bit.const():
            return True

        return bit in self.value_map

    def get_value(self, bit):
        if isinstance(bit, ArrayType):
            return [self.get_value(b) for b in bit]

        if bit.isinput():
            bit = bit.value()

        if bit.const():
            return True if bit == VCC else False

        return self.value_map[bit]

    def set_value(self, bit, newval):
        if isinstance(bit, ArrayType):
            for b,v in zip(bit, newval):
                self.set_value(b, v)
            return

        assert isinstance(newval, bool), "Can only set boolean values"
        assert bit.isoutput()

        self.value_map[bit] = newval

class PythonSimulator(CircuitSimulator):
    def __setup_primitives(self):
        wrapped = []
        for primitive in self.circuit.instances:
            wrapped.append(SimPrimitive(primitive, self.value_store))

        return wrapped

    def __setup_circuit(self, clkbit):
        if clkbit:
            self.clkbit = clkbit
        else:
            if hasattr(self.circuit, 'CLKIN'):
                self.clkbit = self.circuit.CLKIN
            elif hasattr(self.circuit, 'CLK'):
                self.clkbit = self.circuit.CLK
            else:
                # assert False, 'No valid clock in circuit'
                self.clkbit = None

        self.circuit_inputs = []
        self.circuit_outputs = []
        for name, bit in self.circuit.interface.ports.items():
            if not isinstance(bit, ArrayType):
                bit = [bit]
            for b in bit:
                if b.isoutput():
                    self.circuit_inputs.append(b)
                    self.value_store.set_value(b, False)
                else:
                    self.circuit_outputs.append(b)

    def __outputs_initialized(self):
        for bit in self.circuit_outputs:
            assert bit.isinput()
            if not self.value_store.value_initialized(bit):
                return False

        return True

    def __get_ordered_primitives(self, unordered_primitives):
        state_primitives = []
        after_state = []

        state_primitives = []
        for primitive in unordered_primitives:
            if primitive.stateful():
                primitive.initialize_outputs()
                state_primitives.append(primitive)

        unordered_primitives[:] = [u for u in unordered_primitives if not u.stateful()]

        combinational = []
        while len(unordered_primitives) > 0:
            found = False
            for primitive in unordered_primitives:
                if primitive.inputs_satisfied():
                    primitive.initialize_outputs()
                    combinational.append(primitive)
                    unordered_primitives.remove(primitive)
                    found = True
                    break
            assert found, "Some circuits have unsatisfied inputs"
        
        return ExecutionOrder(stateful=state_primitives, combinational=combinational)

    def __init__(self, main_circuit, clkbit=None):
        setup_clocks(main_circuit)
        self.txfm = flatten(main_circuit)
        self.circuit = self.txfm.circuit
        self.value_store = ValueStore()
        self.__setup_circuit(clkbit)
        self.watchpoints = []

        primitives = self.__setup_primitives()

        self.execution_order = self.__get_ordered_primitives(primitives)

        assert self.__outputs_initialized(), "All circuit outputs not initialized."

    def get_capabilities(self):
        return []

    def get_value(self, bit, scope):
        if not isinstance(scope, Scope):
            raise PythonSimulatorException("Second argument to `get_value` should be an instance of Scope")
        newbit = self.txfm.get_new_bit(bit, scope)
        if newbit is None:
            return None

        try:
            return self.value_store.get_value(newbit)
        except KeyError:
            return None

    def set_value(self, bit, scope, newval):
        if not isinstance(scope, Scope):
            raise PythonSimulatorException("Second argument to `set_value` should be an instance of Scope, not {}".format(type(scope)))
        newbit = self.txfm.get_new_bit(bit, scope)
        if not self.is_circuit_input(newbit):
            message = "Only setting main's inputs is supported (Trying to set: {})".format(bit)
            raise PythonSimulatorException(message)
        else:
            self.value_store.set_value(newbit, newval)

    def is_circuit_input(self, value):
        """
        Checks if `value` is in `self.circuit_inputs`.
        If `value` is an `ArrayType`, it recursively checks the elements
        """
        if isinstance(value, BitType):
            return value in self.circuit_inputs
        elif isinstance(value, ArrayType):
            return all(self.is_circuit_input(elem) for elem in value)
        else:
            raise NotImplementedError(type(value))

    def evaluate(self):
        for primitive in self.execution_order.stateful:
            primitive.simulate()
        for primitive in self.execution_order.combinational:
            primitive.simulate()

        triggered = []
        for watch in self.watchpoints:
            if watch.was_triggered():
                triggered.append(watch)

        return ExecutionState(triggered_points=triggered, clock=self.get_clock_value(), cycles=0)

    def get_clock_value(self):
        """
        Looks up the value of `self.clkbit` in `self.value_store`
        Returns None if self.clkbit is None (circuit doesn't have a clock)
        """
        if self.clkbit is not None:
            return self.value_store.get_value(self.clkbit)
        return None

    def step(self):
        if self.clkbit is not None:
            cur_clock_val = self.value_store.get_value(self.clkbit)
            self.value_store.set_value(self.clkbit, not cur_clock_val)

    def cont(self):
        cycles = 0
        while True:
            self.step()
            state = self.evaluate()
            if not state.clock:
                cycles += 1

            if state.triggered_points:
                return ExecutionState(triggered_points=state.triggered_points, clock=state.clock, cycles=cycles)

    def add_watchpoint(self, bit, scope, value=None):
        self.watchpoints.append(WatchPoint(bit, scope, self, value))
        return self.watchpoints[-1].idx

    def delete_watchpoint(self, num):
        for w in self.watchpoints:
            if w.idx == num:
                del w
                return True

        return False
